import psycopg
from psycopg_pool import ConnectionPool
import atexit

def getDb():
    DSN = "postgresql://postgres:database_system_provide_reliability@localhost:5432/postgres"

    pool = ConnectionPool(DSN)
    
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1, current_database(), current_user, version()")
            print(cur.fetchone())
    
    return pool