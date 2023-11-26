import psycopg2 as psy
import logging


def Connection():
    try:
        connect = psy.connect(host="127.0.0.1", dbname="postgres", user="postgres", password="hp14b7860")
        print("Successfully connected to the PostgreSQL database")
        # Set autocommit to True to avoid running the CREATE DATABASE inside a transaction
        connect.set_session(autocommit=True)
        return connect
    except psy.Error as e:
        print("Error couldn't make a connection to the PostgreSQL database")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error connecting to PostgreSQL: {e}')
        return None


def DB():
    conn = Connection()
    if conn:
        try:
            # Perform operations with the PostgreSQL connection
            cursor = conn.cursor()

            # Example: Create a database if it does not exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS STUDENT_INFO")

            # Check if the database was created successfully
            cursor.execute("SELECT datname FROM pg_database WHERE datname='STUDENT_INFO'")
            result = cursor.fetchone()
            if result:
                print("Database STUDENT_INFO created successfully")
                logging.info("Database STUDENT_INFO created successfully")
            else:
                print("Database creation failed")
                logging.error("Database creation failed")

            cursor.close()
        except psy.Error as e:
            print("Error executing SQL query")
            logging.basicConfig(filename='QueryError_log.txt', level=logging.ERROR,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f'Error executing SQL query: {e}')
        finally:
            conn.close()


if __name__ == "__main__":
    DB()  # calls the DB function.
