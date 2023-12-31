import psycopg2 as psy
import logging

# Configure logging once at the beginning
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_postgres():
    try:
        connection = psy.connect(host="127.0.0.1", dbname="postgres", user="postgres", password="root")
        connection.set_session(autocommit=True)
        print("Successfully connected to the PostgreSQL database")
        return connection

    except psy.Error as e:
        error_message = "Error connecting to PostgreSQL database"
        print(error_message)
        logging.error(f'{error_message}: {e}')
        raise e


def create_database(connection, database_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
            database_exists = cursor.fetchone() is not None

            if not database_exists:
                cursor.execute(f"CREATE DATABASE {database_name}")
                print(f"Database '{database_name}' created successfully.")
            else:
                print(f"Database '{database_name}' already exists")

    except psy.Error as e:
        error_message = f"Error creating the database '{database_name}': {e}"
        print(error_message)
        logging.error(error_message)
        raise e


def check_database_existence(connection, database_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        database_exists = cursor.fetchone() is not None
        if database_exists:
            print("Database exists.")
        else:
            print("DB doesn't exist.")
        return database_exists


def create_table(connection, table_, columns):
    try:
        with connection.cursor() as cursor:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_} ("

            for col, data_type in columns.items():
                create_table_query += f"{col} {data_type}, "

            create_table_query = create_table_query.rstrip(', ')
            create_table_query += ");"

            cursor.execute(create_table_query)
            print(f"Table '{table_}' created successfully.")

    except psy.Error as e:
        error_message = f"Error creating table '{table_}': {e}"
        print(error_message)
        logging.error(error_message)
        raise e


def check_table_existence(connection, table):
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table,))
        table_exists = cursor.fetchone()[0]
        if table_exists:
            print("Table exists.")

        else:
            print("Table doesn't exist.")
        return table_exists


def add_data_to_table(connection, data, tablename):
    try:
        with connection.cursor() as cursor:
            data_length = len(list(data.values())[0])

            for i in range(data_length):
                values = [data[column][i] for column in data]
                placeholders = ', '.join(['%s'] * len(values))

                insert_query = f"INSERT INTO {tablename} ({', '.join(data.keys())}) VALUES ({placeholders});"
                cursor.execute(insert_query, tuple(values))

            print(f"Data added to the table '{tablename}' successfully.")

    except psy.Error as e:
        error_message = f"Error adding data to table '{tablename}': {e}"
        print(error_message)
        logging.error(error_message)
        raise e


# Example usage
if __name__ == "__main__":
    try:
        postgres_connection = connect_to_postgres()
        database_name = "student_data"
        if not check_database_existence(postgres_connection, database_name):
            create_database(postgres_connection, database_name)

        table_name = "Student"
        table_columns = {
            "Student_ID": "SERIAL PRIMARY KEY",
            "Student_Age": "INTEGER",
            "Student_Name": "VARCHAR(255)",
            "Phone": "BIGINT"
        }

        if not check_table_existence(postgres_connection, table_name):
            create_table(postgres_connection, table_name, table_columns)

        sample_data = {
            "Student_Age": [25, 24],
            "Student_Name": ["John Doe", "Archit Sood"],
            "Phone": [1234567890, 3284883274]
        }

        add_data_to_table(postgres_connection, sample_data, table_name)

    except psy.Error as e:
        print("An error occurred.")
        # Handle the exception as needed.
    finally:
        if postgres_connection:
            postgres_connection.close()
