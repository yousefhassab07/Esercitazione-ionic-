from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app) # Abilita richieste dal frontend (Angular/Ionic)

db = DatabaseWrapper()

@app.route('/')
def index():
    return "Sushi Backend is Running!"

# --- API MENU ---
@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(db.get_all_categories())

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(db.get_menu_items())

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    db.add_product(data['name'], data['price'], data['category_id'], data['image_url'])
    return jsonify({"message": "Product added"}), 201

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    db.delete_product(id)
    return jsonify({"message": "Product deleted"}), 200

# --- API ORDINI CLIENTE ---
@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.json
    # data: { "table_code": "T1", "customer_name": "Mario", "items": [{"product_id": 1, "quantity": 2}] }
    table = data.get('table_code')
    user = data.get('customer_name')
    items = data.get('items', [])
    
    # Assicuriamoci che il tavolo esista (opzionale, ma buona prassi)
    db.create_table_session(table, user)
    
    for item in items:
        db.add_order(table, user, item['product_id'], item['quantity'])
        
    return jsonify({"message": "Order placed"}), 201

@app.route('/api/orders/<string:table_code>', methods=['GET'])
def get_table_orders(table_code):
    orders = db.get_orders_by_table(table_code)
    return jsonify(orders)

# --- API STAFF ---
@app.route('/api/staff/orders', methods=['GET'])
def get_all_orders():
    orders = db.get_all_orders_staff()
    return jsonify(orders)

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    data = request.json
    new_status = data.get('status')
    db.update_order_status(order_id, new_status)
    return jsonify({"message": "Status updated"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
