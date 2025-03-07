import datetime as dt
import psycopg

from simple_rate_limiter.backends.base import BaseBackend
from simple_rate_limiter.backends.record import Record
from simple_rate_limiter.rate import Rate


class Queries:
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        key TEXT PRIMARY KEY,
        window_start TIMESTAMPTZ NOT NULL,
        prev_count INT NOT NULL,
        count INT NOT NULL
    );
    """

    LOCK = """
    SELECT * FROM {table_name} WHERE KEY = %s FOR UPDATE;
    """

    INSERT = """
    INSERT INTO {table_name} (key, window_start, prev_count, count)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (key) DO UPDATE
    SET window_start = EXCLUDED.window_start,
        prev_count = EXCLUDED.prev_count,
        count = EXCLUDED.count
    """

    SELECT = """
    SELECT window_start, prev_count, count
    FROM {table_name}
    WHERE key = %s
    """


class PostgresBackend(BaseBackend):
    def __init__(self, conn: psycopg.Connection, table_name: str):
        self.conn = conn
        self.table_name = table_name
        self._create_table()

    def _create_table(self):
        with self.conn.cursor() as cur:
            cur.execute(Queries.CREATE_TABLE.format(table_name=self.table_name))


    def _try_acquire(self, rate: Rate, key: str, num_tokens: int, require_all: bool) -> int | bool:
        with self.conn.cursor() as cur:
            self._lock_key(cur, key)
            now = dt.datetime.now(dt.UTC)
            record = self._retrieve_record(cur, key, now, rate)
            allowed = self.get_allowed(now, num_tokens, rate, record)

            if require_all and allowed != num_tokens:
                return False

            record.count += allowed
            if allowed > 0:
                self._insert_record(cur, key, record)
                self.conn.commit()

        return allowed if not require_all else True

    def _lock_key(self, cur, key):
        cur.execute(Queries.LOCK.format(table_name=self.table_name), (key,))

    def _retrieve_record(self, cur, key, now, rate):
        cur.execute(Queries.SELECT.format(table_name=self.table_name), (key,))
        if cur.rowcount > 0:
            window_start, prev_count, count = cur.fetchone()
        else:
            window_start = now
            prev_count = 0
            count = 0
        record = Record(window_start, prev_count, count)
        record.sync(rate, now)
        return record

    def _insert_record(self, cur, key, record):
        cur.execute(
            Queries.INSERT.format(table_name=self.table_name),
            (key, record.window_start, record.prev_count, record.count),
        )
