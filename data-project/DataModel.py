import psycopg2 as psy
import logging


def Connection():
    try:
        connect = psy.connect(host="127.0.0.1", dbname="postgres", user="postgres",
                              password="hp14b7860")
        print("Successfully connected to the PostgreSQL database")
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
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        database_exists = cursor.fetchone() is not None

        if not database_exists:
            print(f"Database {database_name} does not exist. Creating...")
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database {database_name} created successfully")

    except psy.Error as e:
        print("Error creating the database")
        logging.basicConfig(filename='QueryError_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error creating the database: {e}')
    finally:
        cursor.close()


def add_data_to_table(conn, table_name, data):
    try:
        cursor = conn.cursor()

        # Example: Insert data into a table
        insert_query = f"INSERT INTO {table_name} (name, age, gender, subject, marks) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (data['name'], data['age'], data['gender'], data['subject'], data['marks']))

        print("Data added to the table successfully")
        logging.info("Data added to the table: %s", data)

        cursor.close()
    except psy.Error as e:
        print("Error executing SQL query")
        logging.basicConfig(filename='QueryError_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error executing SQL query: {e}')


def query(database_name, table_name, data):
    connect = Connection()

    if connect:
        try:
            create_database(connect, database_name)

            # Check if the table exists and has data
            cursor = connect.cursor()
            cursor.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1);")
            table_has_data = cursor.fetchone()[0]

            if not table_has_data:
                print(f"Table {table_name} either does not exist or has no data. Creating and adding data...")

                # Create the table
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        student_id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        age INTEGER,
                        gender VARCHAR(10),
                        subject VARCHAR(255),
                        marks FLOAT
                    );
                ''')

                print("Table created successfully")

                # Add data to the table
                add_data_to_table(connect, table_name, data)

            elif table_has_data:
                print(f"Table {table_name} has data. No need to create or add data.")
            else:
                cursor.execute("select * from student_info limit 5;")
        finally:
            connect.close()


# Example usage
if __name__ == "__main__":
    database_name = "your_database"
    table_name = "student_info"
    sample_data = [
        {'name': 'Alice Smith', 'age': 22, 'gender': 'Female', 'subject': 'Physics', 'marks': 78.5},
        {'name': 'Bob Johnson', 'age': 21, 'gender': 'Male', 'subject': 'Chemistry', 'marks': 92.0},
        {'name': 'Eva Williams', 'age': 23, 'gender': 'Female', 'subject': 'Biology', 'marks': 87.5},
        {'name': 'Charlie Brown', 'age': 20, 'gender': 'Male', 'subject': 'History', 'marks': 65.0},
        {'name': 'Grace Davis', 'age': 22, 'gender': 'Female', 'subject': 'Computer Science', 'marks': 89.5}
    ]
    # Perform operations with the PostgreSQL connection
    query(database_name, table_name, sample_data)
