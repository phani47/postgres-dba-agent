from app.db.postgres import get_connection


with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        result = cur.fetchone()

        print(result)