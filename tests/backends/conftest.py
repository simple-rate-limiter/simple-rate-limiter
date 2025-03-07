import pytest
import os

from simple_rate_limiter.backends.in_memory import InMemoryBackend

PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]


@pytest.fixture(scope="session")
def postgres_conn():
    import psycopg

    conn = psycopg.connect(f"host={PG_HOST} port={PG_PORT} dbname={DB_NAME} user={PG_USER} password={PG_PASSWORD}")
    yield conn
    conn.close()


@pytest.fixture
def postgres_backend(postgres_conn):
    from simple_rate_limiter.backends.postgres import PostgresBackend

    table_name = "rate_limits"
    backend = PostgresBackend(postgres_conn, table_name)
    yield backend
    with postgres_conn.cursor() as cur:
        cur.execute(f"DROP TABLE {table_name}")
        postgres_conn.commit()


@pytest.fixture
def in_memory_backend():
    return InMemoryBackend()


@pytest.fixture(params=["postgres", "in_memory"])
def backend(request, postgres_backend, in_memory_backend):
    """Fixture that provides different backend implementations."""
    if request.param == "postgres":
        return postgres_backend
    if request.param == "in_memory":
        return in_memory_backend
    raise ValueError(f"Unknown backend: {request.param}")
