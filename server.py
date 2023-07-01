from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.String(100), nullable=True)
    sales = db.Column(db.PickleType, nullable=True) # We use PickleType to store an array.
    categories = db.Column(db.PickleType, nullable=True) # We use PickleType to store an array.
    brand = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'], 
        description=data['description'], 
        price=data['price'], 
        image_url=data['image_url'], 
        quantity=data['quantity'], 
        supplier_id=data['supplier_id'], 
        sales=data.get('sales', []),  # Default to an empty list if not provided
        categories=data.get('categories', []),  # Default to an empty list if not provided
        brand=data['brand'], 
        model=data['model']
    )
    db.session.add(new_product)
    db.session.commit()
    return {"message": f"product {new_product.name} has been created successfully."}, 201

@app.route('/update_product/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get(product_id)
    if product is None:
        return {"error": "Product not found"}, 404

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)
    product.quantity = data.get('quantity', product.quantity)
    product.supplier_id = data.get('supplier_id', product.supplier_id)
    product.sales = data.get('sales', product.sales)
    product.categories = data.get('categories', product.categories)
    product.brand = data.get('brand', product.brand)
    product.model = data.get('model', product.model)
    
    db.session.commit()
    return {"message": f"product {product.name} has been updated successfully."}, 200


@app.route("/remove_product/<product_id>", methods=["DELETE"])
def remove_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product removed"}, 200
    else:
        return {"error": "Product not found"}, 404

@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    products_list = [
        {
            "id": p.id, 
            "name": p.name, 
            "description": p.description, 
            "price": p.price, 
            "image_url": p.image_url, 
            "quantity": p.quantity,
            "brand": p.brand, 
            "model": p.model, 
            "categories": p.categories, 
            "sales": p.sales,
            "supplier_id": p.supplier_id,
        } 
        for p in products
    ]
    return {"products": products_list}, 200

@app.route('/add_category/<product_id>', methods=['PUT'])
def add_category(product_id):
    data = request.get_json()
    category = data.get('category')

    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    if not product.categories:
        product.categories = []
        
    product.categories.append(category)
    
    db.session.commit()
    
    return {'message': f'Category successfully added to product {product_id}'}, 200

@app.route('/update_all_products', methods=['PUT'])
def update_all_products():
    data = request.get_json()

    # We assume that all products will have the same new data.
    # If the value is not provided for a particular field, we leave the old value.
    products = Product.query.all()
    for product in products:
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.image_url = data.get('image_url', product.image_url)
        product.quantity = data.get('quantity', product.quantity)
        product.supplier_id = data.get('supplier_id', product.supplier_id)
        product.sales = data.get('sales', product.sales)
        product.categories = data.get('categories', product.categories)
        product.brand = data.get('brand', product.brand)
        product.model = data.get('model', product.model)

    db.session.commit()
    return {"message": "All products have been updated successfully."}, 200



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)