export PG_CONTAINER_NAME=${PG_CONTAINER_NAME:-rate_limiter_pg}  # Default container name
export PG_HOST=${PG_HOST:-127.0.0.1} # Host for PostgreSQL to run on
export PG_PORT=${PG_PORT:-5432}  # Port for PostgreSQL to listen on
export PG_USER=${PG_USER:-rate_limiter}  # PostgreSQL user name
export PG_PASSWORD=${PG_PASSWORD:-rate_limiter}  # Password for the PostgreSQL user
export DB_NAME=${DB_NAME:-rate_limiter}  # Name of the database to create