import psycopg2 as psy
import logging


def Connection():
    global connect
    try:
        connect = psy.connect("host=127.0.0.1 dbname=postgres user=postgres password=hp14b7860")
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

            # Example: Create a database (ensure you have the necessary privileges)
            cursor.execute("CREATE DATABASE IF NOT EXISTS STUDENT_INFO")

            # Commit changes to the database
            conn.commit()

            # Example: Select data from a table (replace 'your_table' with an actual table name)
            cursor.execute("SELECT * FROM your_table")
            result = cursor.fetchall()
            print(result)

            cursor.close()
        except psy.Error as e:
            print("Error executing SQL query")
            logging.basicConfig(filename='QueryError_log.txt', level=logging.ERROR,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f'Error executing SQL query: {e}')
        finally:
            conn.close()


if __name__ == "__main__":
    DB()  # calls the DB function. Just fix errors, don't change the code.

