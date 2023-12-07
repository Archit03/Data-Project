import psycopg2 as psy
import logging


def log():
    logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def connection():
    try:
        with psy.connect(host="127.0.0.1", dbname="postgres", user="postgres", password="root") as conn:
            print("Successfully connected to the PostgreSQL database")
            conn.set_session(autocommit=True)
            return conn
    except psy.Error as e:
        print("Error connecting to PostgreSQL database")
        logging.error(f'Error connecting to PostgreSQL: {e}')
        log()
        return None


def create_database(conn, database_name):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        database_exists = cursor.fetchone() is not None

        if not database_exists:
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database {database_name} created successfully")
        else:
            print(f"Database {database_name} already exists")

    except psy.Error as e:
        print("Error creating the database")
        logging.error(f'Error creating the database: {e}')
    finally:
        if cursor:
            cursor.close()


def create_table(conn, table_name, columns):
    cursor = conn.cursor()
    try:
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        create_table_query += ', '.join([f"{col} {data_type}" for col, data_type in columns.items()])
        create_table_query += ");"

        cursor.execute(create_table_query)

        if cursor.rowcount == -1:  # Check if the last operation affected a row (returns -1 for DDL statements)
            print(f"Table '{table_name}' created successfully.")
            conn.commit()
        else:
            print("Table not created.")
    except psy.Error as e:
        error_message = f"Error creating table '{table_name}': {e}"
        print(error_message)
        logging.error(error_message)
        raise e
    finally:
        if cursor:
            cursor.close()


"""
def add_data_to_table(conn, data, table_name):
    with conn.cursor() as cursor:
        try:
            keys = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))

            for values in zip(*data.values()):
                insert_query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders});"
                cursor.execute(insert_query, values)

            conn.commit()

            print(f"Data added to the table '{table_name}' successfully.")

        except psy.Error as e:
            error_message = f"Error adding data to table '{table_name}': {e}"
            print(error_message)
            logging.error(error_message)
            raise e


def query():
    return None
"""

# Example usage
if __name__ == "__main__":
    log()
    connection_ = connection()  # Get a PostgreSQL connection
    columns_ = {
        "Student_ID": "SERIAL PRIMARY KEY",
        "Student_Age": "INTEGER",
        "Student_Name": "VARCHAR(255)",
        "Phone": "BIGINT"
    }

    sample_data_ = {
        "Student_Age": [25, 24],
        "Student_Name": ["John Doe", "Archit Sood"],
        "Phone": [1234567890, 3284883274]
    }

    tablename_ = "Student"
    if connection_:
        create_database(connection_, "student_data")
        create_table(connection_, tablename_, columns_)
        # add_data_to_table(connection_, sample_data_, tablename_)
        connection_.close()  # Close the connection when done
