from faker import Faker
import random
import requests

fake = Faker()
server_url = 'http://localhost:5000'

def add_product(name, description, price, image_url, quantity, supplier_id, sales, categories, brand, model):
    data = {
        "name": name,
        "description": description,
        "price": price,
        "image_url": image_url,
        "quantity": quantity,
        "supplier_id": supplier_id,
        "sales": sales,
        "categories": categories,
        "brand": brand,
        "model": model
    }
    response = requests.post(f'{server_url}/add_product', json=data)
    return response.json()['message']

def generate_product():
    name = fake.word()
    description = fake.sentence()
    price = round(random.uniform(10, 500), 2)
    random_id = random.randint(1, 1000)  # Generate a random number for the ID
    image_url = f"https://picsum.photos/id/{random_id}/300/200"
    quantity = random.randint(0, 100)
    supplier_id = fake.random_int(min=1, max=5)
    sales = [random.randint(0, 50) for _ in range(6)]  # Random sales data for the last 6 months
    categories = [fake.word() for _ in range(random.randint(1, 3))]  # Random number of categories
    brand = fake.word()
    model = fake.word()

    result = add_product(name, description, price, image_url, quantity, supplier_id, sales, categories, brand, model)
    print(result)

def populate_database(num_products):
    print("Populating database...")
    for _ in range(num_products):
        generate_product()
    print("Database populated successfully.")

populate_database(30)  # Change the value as per your requirement
