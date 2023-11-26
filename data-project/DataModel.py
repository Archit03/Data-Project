import psycopg2 as psy
import logging


def Connection():
    global connect
    try:
        connect = psy.connect("host=127.0.0.1 dbname=postgres user=postgres password=hp14b7860")
        return connect
    except psy.Error as e:
        print("Error couldn't make a connection to the PostgresSQL database")
        logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error connecting to PostgresSQL: {e}')
    try:
        cur = connect.cursor()
    except psy.Error as e:
        print("Error couldn't make a connection to the PostgresSQL database")
        logging.basicConfig(filename='CursorError_log.txt', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'Error connecting to Cursor: {e}')
        connect.set_session(autocommit=True)
        return None


def DB():
    conn = Connection()
    if conn:
        # Perform operations with the PostgresSQL connection
        # For example, create a cursor and execute queries
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE STUDENT_INFO")
        cursor.execute("SELECT * FROM your_table")
        result = cursor.fetchall()
        print(result)
        cursor.close()
        conn.close()


if __name__ == "__main__":
    DB()  # calls the DB function.
