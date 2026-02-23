from flask import Flask, jsonify
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
# La configurazione CORS più semplice possibile
CORS(app)

db = DatabaseWrapper()

@app.route('/')
def index():
    return "Sushi Backend is Running!"

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(db.get_menu_items())

@app.route('/api/orders/<string:table_code>', methods=['GET'])
def get_table_orders(table_code):
    orders = db.get_orders_by_table(table_code)
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
