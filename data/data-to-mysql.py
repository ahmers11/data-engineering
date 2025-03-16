import mysql.connector
from mysql.connector import Error
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Function to connect to MySQL and create the OLTP database
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",    # Change if needed
            user="root",         # Change if needed
            password="panther1"  # Change to your MySQL password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS OLTP")
            cursor.execute("USE OLTP")
            return connection, cursor
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None, None

# Function to create necessary tables
def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            cust_id VARCHAR(36) PRIMARY KEY,
            cust_first_name VARCHAR(50),
            cust_last_name VARCHAR(50),
            cust_address TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(36) PRIMARY KEY,
            product_name VARCHAR(100),
            price DECIMAL(10,2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            trans_id VARCHAR(36) PRIMARY KEY,
            trans_date DATE,
            trans_amt DECIMAL(10,2),
            cust_id VARCHAR(36),
            product_id VARCHAR(36),
            FOREIGN KEY (cust_id) REFERENCES customers(cust_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        )
    """)

# Function to insert data into MySQL tables
def insert_data(cursor, connection, table, data):
    if not data:
        return

    # Generating query dynamically based on keys
    columns = ", ".join(data[0].keys())
    values_placeholders = ", ".join(["%s"] * len(data[0]))

    query = f"INSERT INTO {table} ({columns}) VALUES ({values_placeholders})"

    values = [tuple(d.values()) for d in data]

    cursor.executemany(query, values)
    connection.commit()

# Function to generate fake customer data
def generate_customer_data(num_customers=10):
    return [{
        'cust_id': fake.uuid4(),
        'cust_first_name': fake.first_name(),
        'cust_last_name': fake.last_name(),
        'cust_address': fake.address().replace("\n", ", ")  # Clean up address
    } for _ in range(num_customers)]

# Function to generate fake product data
def generate_product_data(num_products=10):
    return [{
        'product_id': fake.uuid4(),
        'product_name': fake.word(),
        'price': round(random.uniform(10.0, 500.0), 2)
    } for _ in range(num_products)]

# Function to generate fake transaction data
def generate_transaction_data(customers, products, num_transactions=50):
    return [{
        'trans_id': fake.uuid4(),
        'trans_date': fake.date_between(start_date='-1y', end_date='today'),
        'trans_amt': round(random.uniform(10.0, 1000.0), 2),
        'cust_id': random.choice(customers)['cust_id'],  # FK to customer
        'product_id': random.choice(products)['product_id']  # FK to product
    } for _ in range(num_transactions)]

# Main Execution
if __name__ == "__main__":
    # Connect to MySQL
    connection, cursor = connect_to_mysql()
    
    if connection and cursor:
        create_tables(cursor)

        # Generate data
        customers = generate_customer_data(num_customers=100)
        products = generate_product_data(num_products=50)
        transactions = generate_transaction_data(customers, products, num_transactions=500)

        # Insert data
        insert_data(cursor, connection, "customers", customers)
        insert_data(cursor, connection, "products", products)
        insert_data(cursor, connection, "transactions", transactions)

        print("Data inserted into MySQL successfully.")

        # Close connection
        cursor.close()
        connection.close()
