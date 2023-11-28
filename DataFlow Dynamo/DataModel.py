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
    cursor = None
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
        print("Error adding data to the table")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error adding data to the table: {e}')
    finally:
        if cursor:
            cursor.close()


def add_data_to_table(conn, data, table_name):
    cursor = conn.cursor()
    try:
        insert_query = f"INSERT INTO {table_name} ("

        columns = ','.join(data.keys())
        insert_query += f"{columns}) VALUES ("

        values = ','.join(['%s' for _ in data.values()])
        insert_query += f"{values})"

        cursor.execute(insert_query, tuple(data.values()))
        conn.commit()
        print(f"Data added to to the '{table_name}' table successfully")
        pass

    except psy.Error as e:
        print("Error adding data to the table")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error adding data to the table: {e}')
    finally:
        if cursor:
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
        create_database(connection, "student_info")
        create_Table(connection, tablename, columns)
        add_data_to_table(connection, sample_data, tablename)
