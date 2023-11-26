import psycopg2 as psy
import logging


def Connection():
    try:
        connect = psy.connect(host="127.0.0.1", dbname="student_info", user="postgres",
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


def create_table(conn):
    try:
        cursor = conn.cursor()

        # Example: Create a table
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS student_info (
                student_id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                age INTEGER,
                gender VARCHAR(10),
                subject VARCHAR(255),
                marks FLOAT
            );
        '''
        cursor.execute(create_table_query)

        print("Table created successfully")
        logging.info("Table created successfully")

        cursor.close()
    except psy.Error as e:
        print("Error executing SQL query")
        logging.basicConfig(filename='QueryError_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error executing SQL query: {e}')


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


def DB():
    conn = Connection()
    if conn:
        try:
            # Create the table if it doesn't exist
            create_table(conn)

            # Take the table name as input (you can modify this based on your use case)
            table_name = "student_info"

            # Sample data to be added to the table
            data_to_add = {'name': 'John Doe', 'age': 20, 'gender': 'Male', 'subject': 'Math', 'marks': 85.5}

            # Perform operations with the PostgreSQL connection
            add_data_to_table(conn, table_name, data_to_add)

        finally:
            conn.close()


if __name__ == "__main__":
    DB()  # calls the DB function.
