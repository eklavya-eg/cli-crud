import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv('DATABASE_URL')
try:
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()

    schema_name = "clischema"
    create_schema = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
    cursor.execute(create_schema)
    cursor.execute("DROP SCHEMA IF EXISTS public")

    users_table = """
    CREATE TABLE IF NOT EXISTS clischema.users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    """ #users

    search_history_table = """
    CREATE TABLE IF NOT EXISTS clischema.search_history (
        id SERIAL PRIMARY KEY,
        username TEXT REFERENCES clischema.users(username),
        time_monotonic INTEGER NOT NULL,
        search_term TEXT NOT NULL
    );
    """ #search_history

    cursor.execute(users_table)
    cursor.execute(search_history_table)

    connection.commit()

    print("Tables created successfully.")

except Exception as error:
    print(f"error creating tables: {error}")
