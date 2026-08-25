from app.db.postgres import get_connection


def get_database_size():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    current_database(),
                    pg_size_pretty(
                        pg_database_size(current_database())
                    );
            """)

            return cur.fetchone()


def get_active_sessions():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    count(*)
                FROM pg_stat_activity
                WHERE state = 'active';
            """)

            return cur.fetchone()[0]


def get_long_running_queries():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    pid,
                    usename,
                    datname,
                    now() - query_start AS duration,
                    query
                FROM pg_stat_activity
                WHERE state = 'active'
                  AND query_start IS NOT NULL
                  AND now() - query_start > interval '1 minute'
                ORDER BY query_start;
            """)

            return cur.fetchall()

from langchain_core.tools import tool
from app.db.postgres import get_connection


@tool
def get_database_size() -> str:
    """Return the name and size of the current PostgreSQL database."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    current_database(),
                    pg_size_pretty(
                        pg_database_size(current_database())
                    );
            """)

            db_name, db_size = cur.fetchone()

    return f"Database: {db_name}, Size: {db_size}"


@tool
def get_active_sessions() -> str:
    """Return the number of currently active PostgreSQL sessions."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT count(*)
                FROM pg_stat_activity
                WHERE state = 'active';
            """)

            count = cur.fetchone()[0]

    return f"Active sessions: {count}"


@tool
def get_long_running_queries() -> str:
    """Return PostgreSQL queries running for more than one minute."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    pid,
                    usename,
                    datname,
                    now() - query_start AS duration,
                    query
                FROM pg_stat_activity
                WHERE state = 'active'
                  AND query_start IS NOT NULL
                  AND now() - query_start > interval '1 minute'
                ORDER BY query_start;
            """)

            rows = cur.fetchall()

    if not rows:
        return "No long-running queries found."

    return "\n".join(
        f"PID={row[0]}, User={row[1]}, DB={row[2]}, "
        f"Duration={row[3]}, Query={row[4]}"
        for row in rows
    )

@tool
def get_connection_usage() -> str:
    """Return PostgreSQL connection usage and the configured maximum connections."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    count(*) AS current_connections,
                    current_setting('max_connections')::int AS max_connections
                FROM pg_stat_activity;
            """)

            current, maximum = cur.fetchone()

    percentage = (current / maximum) * 100

    return (
        f"Current connections: {current}, "
        f"Max connections: {maximum}, "
        f"Usage: {percentage:.2f}%"
    )


@tool
def get_blocking_sessions() -> str:
    """Return PostgreSQL sessions that are currently blocking other sessions."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    blocking.pid AS blocking_pid,
                    blocked.pid AS blocked_pid,
                    blocking.usename AS blocking_user,
                    blocked.usename AS blocked_user
                FROM pg_stat_activity blocked
                JOIN pg_stat_activity blocking
                    ON blocking.pid = ANY(
                        pg_blocking_pids(blocked.pid)
                    )
                WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;
            """)

            rows = cur.fetchall()

    if not rows:
        return "No blocking sessions found."

    return "\n".join(
        f"Blocking PID={row[0]}, "
        f"Blocked PID={row[1]}, "
        f"Blocking User={row[2]}, "
        f"Blocked User={row[3]}"
        for row in rows
    )