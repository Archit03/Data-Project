

# Import the functions from your code
from DataModel import Connection, create_database, create_Table, add_data_to_table, query


def test_connection():
    print("Testing database connection...")
    connection = Connection()
    assert connection is not None, "Connection failed!"
    print("Connection successful!")


def test_create_database():
    print("Testing create database...")
    connection = Connection()
    create_database(connection, "test_database")
    print("Database creation test successful!")


def test_create_table():
    print("Testing create table...")
    connection = Connection()
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(255)',
        'age': 'INTEGER',
        'gender': 'VARCHAR(10)'
    }
    create_Table(connection, "test_table", columns)
    print("Table creation test successful!")


def test_add_data_to_table():
    print("Testing add data to table...")
    connection = Connection()
    table_name = "test_table"
    data = {'name': 'John Doe', 'age': 25, 'gender': 'Male'}
    add_data_to_table(connection, table_name, data)
    print("Data addition test successful!")


def test_query():
    print("Testing query...")
    connection = Connection()
    table_name = "test_table"
    data = {'name': 'Jane Doe', 'age': 30, 'gender': 'Female'}
    query("test_database", table_name, data)
    print("Query test successful!")


# Run the tests
if __name__ == "__main__":
    test_connection()
    test_create_database()
    test_create_table()
    test_add_data_to_table()
    test_query()
