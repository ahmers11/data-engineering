import csv
from faker import Faker
import random
import os

# Initialize Faker instance
fake = Faker() 

# Function to generate fake customer data
def generate_customer_data(num_customers=10):
    customers = []
    for _ in range(num_customers):
        customer = {
            'cust_id': fake.uuid4(),
            'cust_first_name': fake.first_name(),
            'cust_last_name': fake.last_name(),
            'cust_address': fake.address().replace("\n", ", ")  # Clean up address
        }
        customers.append(customer)
    return customers

# Function to generate fake product data
def generate_product_data(num_products=10):
    products = []
    for _ in range(num_products):
        product = {
            'product_id': fake.uuid4(),
            'product_name': fake.word(),
            'price': round(random.uniform(10.0, 500.0), 2)
        }
        products.append(product)
    return products

# Function to generate fake transaction data
def generate_transaction_data(customers, products, num_transactions=50):
    transactions = []
    for _ in range(num_transactions):
        transaction = {
            'trans_id': fake.uuid4(),
            'trans_date': fake.date_between(start_date='-1y', end_date='today'),
            'trans_amt': round(random.uniform(10.0, 1000.0), 2),
            'cust_id': random.choice(customers)['cust_id'],  # FK to customer
            'product_id': random.choice(products)['product_id']  # FK to product
        }
        transactions.append(transaction)
    return transactions

# Write to CSV
def write_to_csv(data, filepath, fieldnames):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Ensure directory exists
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Generate data
customers = generate_customer_data(num_customers=100)
products = generate_product_data(num_products=50)
transactions = generate_transaction_data(customers, products, num_transactions=500)

# Specify paths to save CSVs
customer_csv_path = './customers.csv'
product_csv_path = './products.csv'
transaction_csv_path = './transactions.csv'

# Write CSVs
write_to_csv(customers, customer_csv_path, ['cust_id', 'cust_first_name', 'cust_last_name', 'cust_address'])
write_to_csv(products, product_csv_path, ['product_id', 'product_name', 'price'])
write_to_csv(transactions, transaction_csv_path, ['trans_id', 'trans_date', 'trans_amt', 'cust_id', 'product_id'])

print("CSV files generated successfully.")