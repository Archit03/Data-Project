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
    connection = Connection()
    try:
        # Connect to the default PostgreSQL database (usually 'postgres')
        connection.set_session(autocommit=True)  # Set autocommit to True to avoid transaction issues
        cursor = connection.cursor()

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
        if connection:
            connection.close()


# Example usage
if __name__ == "__main__":
    connection = Connection()  # Get a PostgreSQL connection
    if connection:
        create_database(connection, "student_info")
