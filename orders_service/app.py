import os
from flask import Flask, jsonify, request
from flasgger import Swagger
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
app.config['SWAGGER'] = {'title': 'Orders Service API', 'uiversion': 3}
swagger = Swagger(app)

# --- НАСТРОЙКА ПОДКЛЮЧЕНИЯ (SQLAlchemy) ---
server = os.getenv('DB_SERVER', 'localhost')
database = os.getenv('DB_DATABASE', 'MicroshopOrders')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# Формируем строку подключения для SQLAlchemy
if username and password:
    # Для GitHub Actions
    conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes'
else:
    # Для Локального ПК (Windows Auth)
    conn_str = f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes'

app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- МОДЕЛЬ (ОПИСАНИЕ ТАБЛИЦЫ В КОДЕ) ---
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # Мы добавим новое поле позже, в миграции №2


# --- РОУТЫ ---
@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Получить список заказов
    ---
    responses:
      200:
        description: Список
    """
    orders = Order.query.all()
    return jsonify([{
        "id": o.id, "product_id": o.product_id,
        "customer_id": o.customer_id, "quantity": o.quantity
    } for o in orders])


@app.route('/orders', methods=['POST'])
def create_order():
    """
    Создать заказ
    ---
    parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            product_id: {type: integer}
            customer_id: {type: integer}
            quantity: {type: integer}
    responses:
      201:
        description: Created
    """
    data = request.json
    new_order = Order(
        product_id=data['product_id'],
        customer_id=data['customer_id'],
        quantity=data['quantity']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"id": new_order.id, "message": "Order created"}), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)

