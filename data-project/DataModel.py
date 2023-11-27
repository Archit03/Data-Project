import psycopg2 as psy
import logging


def Connection():
    try:
        connect = psy.connect(host="127.0.0.1", dbname="postgres", user="postgres",
                              password="root")
        if connect:
            print("Successfully connected to the PostgreSQL database")
        else:
            print("An error occurred, please check the logs.")
        connect.set_session(autocommit=True)  # Set autocommit to True to avoid transaction issues
        return connect
    except psy.Error as e:
        print("Error couldn't make a connection to the PostgreSQL database")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error connecting to PostgreSQL: {e}')
        return None


def create_database(conn, database_name):
    try:
        # Connect to the default PostgreSQL database (usually 'postgres')
        conn.set_session(autocommit=True)  # Set autocommit to True to avoid transaction issues
        cursor = conn.cursor()

        # Check if the database already exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        database_exists = cursor.fetchone() is not None

        if not database_exists:
            # Create the new database
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database {database_name} created successfully")
        else:
            print(f"Database {database_name} already exists")

    except psy.Error as e:
        print("Error creating the database")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error creating the database: {e}')
    finally:
        if conn:
            conn.close()


def create_Table(conn, table_name, column):
    cursor = conn.cursor()
    try:
        cursor = conn.cursor()

        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        for column, data_type in column.items():
            create_table_query += f"{column} {data_type}, "

        create_table_query = create_table_query.rsplit(',')
        create_table_query += ");"
        cursor.execute(create_table_query)

        conn.commit()

        print(f"Table '{table_name}' created successfully.")

    except psy.Error as e:
        error_message = f"Error creating table '{table_name}': {e}"
        print(error_message)
        logging.error(error_message)

    finally:
        cursor.close()


def add_data_to_table(conn, data, table_name):
    conn = conn.cursor()


def query():
    return None


# Example usage
if __name__ == "__main__":
    connection = Connection()  # Get a PostgreSQL connection
    columns = {
        "Student_ID": "INTEGER PRIMARY KEY",
        "Student_Age": "INTEGER",
        "Student_Name": "VARCHAR",
        "Phone": "BIGINT"
    }
    if connection:
        create_database(connection, "student_info")
        if create_database:
            create_Table(connection, "Student", columns)
