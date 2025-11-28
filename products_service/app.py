import yaml  # Импортируем библиотеку для работы с YAML
from flask import Flask, jsonify

app = Flask(__name__)

# ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ
def load_products():
    """Читает данные из файла products.yaml"""
    try:
        with open('products.yaml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            # Возвращаем только список items из файла
            return data.get('items', [])
    except FileNotFoundError:
        return []
    except yaml.YAMLError as e:
        print(f"Ошибка в синтаксисе YAML: {e}")
        return []

# Данные товаров (в реальном приложении это была бы база данных)
products = load_products()

@app.route('/products', methods=['GET'])
def get_products():
    """Получить список всех товаров"""
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить товар по ID"""
    product = next((prod for prod in products if prod["id"] == product_id), None)
    return jsonify(product) if product else ('Not Found', 404)

if __name__ == '__main__':
    app.run(port=5001, debug=True)