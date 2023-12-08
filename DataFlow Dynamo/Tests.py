from DataModel import connect_to_postgres, create_database, create_table, add_data_to_table


def test_connection():
    print("Testing database connection...")
    connection = connect_to_postgres()
    assert connection is not None, "Connection failed!"
    print("Connection successful!")


def test_create_database():
    print("Testing create database...")
    connection = connect_to_postgres()
    create_database(connection, "test_database")
    print("Database creation test successful!")


def test_create_table():
    print("Testing create table...")
    connection = connect_to_postgres()
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(255)',
        'age': 'INTEGER',
        'gender': 'VARCHAR(10)'
    }
    create_table()(connection, "test_table", columns)
    print("Table creation test successful!")


def test_add_data_to_table():
    print("Testing add data to table...")
    connection = connect_to_postgres()
    table_name = "test_table"
    data = {'name': 'John Doe', 'age': 25, 'gender': 'Male'}
    add_data_to_table(connection, data, table_name)  # Corrected the parameter order
    print("Data addition test successful!")


def test_query():
    print("Testing query...")
    # Modify this function based on your query testing requirements
    pass


# Run the tests
if __name__ == "__main__":
    try:
        test_connection()
        test_create_database()
        test_create_table()
        test_add_data_to_table()
        test_query()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection after all tests are done
        connection = connect_to_postgres()
        if connection:
            connection.close()
