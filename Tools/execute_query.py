import psycopg2
from typing import Any

def execute_query(sql_query: str, db_config: dict) -> Any:

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                results = cur.fetchall()
                return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
