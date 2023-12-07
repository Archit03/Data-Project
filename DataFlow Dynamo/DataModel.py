import psycopg2 as psy
import logging


def Connection():
    try:
        connect = psy.connect(host="127.0.0.1", dbname="postgres", user="postgres", password="root")
        if connect:
            print("Successfully connected to the PostgreSQL database")
        else:
            print("An error occurred, please check the logs.")
        connect.set_session(autocommit=True)  # Set autocommit to True to avoid transaction issues
        return connect
    except psy.Error as e:
        print("Error connecting to PostgreSQL database")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error connecting to PostgreSQL: {e}')
        return None


def create_database(conn, database_name):
    cursor = conn.cursor()
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
        if cursor:
            cursor.close()


def create_Table(conn, table_name, column):
    cursor = conn.cursor()
    try:
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        for col, data_type in column.items():
            create_table_query += f"{col} {data_type}, "

        create_table_query = create_table_query.rstrip(', ')
        create_table_query += ");"
        cursor.execute(create_table_query)

        conn.commit()

        print(f"Table '{table_name}' created successfully.")

    except psy.Error as e:
        error_message = f"Error creating table '{table_name}': {e}"
        print(error_message)
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(error_message)
        # Raise the exception again to propagate it to the calling code
        raise e

    finally:
        if cursor:
            cursor.close()


def add_data_to_table(conn, data, table_name):
    cursor = conn.cursor()

    try:
        # Assuming all lists in data have the same length
        data_length = len(list(data.values())[0])

        for i in range(data_length):
            values = [data[column][i] for column in data]
            placeholders = ', '.join(['%s'] * len(values))

            # Construct the INSERT query
            insert_query = f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({placeholders});"

            # Execute the query
            cursor.execute(insert_query, tuple(values))
            conn.commit()

        print(f"Data added to the table '{table_name}' successfully.")

    except psy.Error as e:
        error_message = f"Error adding data to table '{table_name}': {e}"
        print(error_message)
        logging.error(error_message)

    finally:
        cursor.close()


def query():
    return None


# Example usage
if __name__ == "__main__":
    connection = Connection()  # Get a PostgreSQL connection
    columns = {
        "Student_ID": "SERIAL PRIMARY KEY",
        "Student_Age": "INTEGER",
        "Student_Name": "VARCHAR(255)",
        "Phone": "BIGINT"
    }

    sample_data = {
        "Student_Age": [25, 24],
        "Student_Name": ["John Doe", "Archit Sood"],
        "Phone": [1234567890, 3284883274]
    }

    tablename = "Student"
    if connection:
        create_database(connection, "student_data")
        create_Table(connection, tablename, columns)
        add_data_to_table(connection, sample_data, tablename)