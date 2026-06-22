import firebase_admin
from firebase_admin import credentials
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

# -------------------------------
# Firebase Init
# -------------------------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# -------------------------------
# DB Connection
# -------------------------------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "@Bhavya12"),
        database=os.getenv("DB_NAME", "project_dbms")
    )

# -------------------------------
# API 1: Store / Update User
# -------------------------------
@app.route('/store_user', methods=['POST'])
def store_user():
    try:
        data = request.json

        name = data.get('name')
        email = data.get('email')
        uid = data.get('uid')

        if not uid or not name or not email:
            return jsonify({"error": "Missing data"}), 400

        db = get_db()
        cursor = db.cursor()

        # check if user exists
        cursor.execute("SELECT user_id FROM user WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            # UPDATE
            cursor.execute("""
                UPDATE user
                SET name = %s
                WHERE email = %s
            """, (name, email))
        else:
            # INSERT
            cursor.execute("""
                INSERT INTO user (name, email, firebase_uid)
                VALUES (%s, %s, %s)
            """, (name, email, uid))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"message": "User stored successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# API 2: Get User by UID
# -------------------------------
@app.route('/get_user/<uid>', methods=['GET'])
def get_user(uid):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, name, email, country_code, phone_number
        FROM user
        WHERE firebase_uid = %s
    """, (uid,))

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


# -------------------------------
# GET ALL PRODUCTS
# -------------------------------
@app.route('/get_products', methods=['GET'])
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.p_id, p.p_name, p.price,
               v.variant_id, v.size_id, v.color_id, v.stock_qty
        FROM product p
        LEFT JOIN product_variant v ON p.p_id = v.p_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    products = {}

    for row in rows:
        p_id = row['p_id']

        if p_id not in products:
            products[p_id] = {
                "p_id": p_id,
                "p_name": row["p_name"],
                "price": row["price"],
                "variants": []
            }

        if row["variant_id"]:
            products[p_id]["variants"].append({
                "variant_id": row["variant_id"],
                "size_id": row["size_id"],
                "color_id": row["color_id"],
                "stock_qty": row["stock_qty"]
            })

    return jsonify(list(products.values()))


# -------------------------------
# GET PRODUCT BY ID
# -------------------------------
@app.route('/get_product/<p_id>', methods=['GET'])
def get_product(p_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT p_id, p_name, description, price
        FROM product
        WHERE p_id = %s
    """, (p_id,))
    product = cursor.fetchone()

    if not product:
        cursor.close()
        db.close()
        return jsonify({"error": "Product not found"}), 404

    cursor.execute("""
        SELECT variant_id, size_id, color_id, stock_qty
        FROM product_variant
        WHERE p_id = %s
    """, (p_id,))

    variants = cursor.fetchall()

    product["variants"] = variants

    cursor.close()
    db.close()

    return jsonify(product)


# -------------------------------
# SEARCH PRODUCTS
# -------------------------------
@app.route('/search/<query>', methods=['GET'])
def search_products(query):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    words = query.split()
    conditions = []
    values = []

    for word in words:
        conditions.append("(p.p_name LIKE %s OR p.description LIKE %s)")
        values.append(f"%{word}%")
        values.append(f"%{word}%")

    sql = f"""
        SELECT DISTINCT p.p_id, p.p_name, p.price
        FROM product p
        JOIN product_variant v ON p.p_id = v.p_id
        WHERE {' OR '.join(conditions)}
    """

    cursor.execute(sql, values)
    result = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(result)


# -------------------------------
# ADD TO CART
# -------------------------------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.json

        user_id = data.get('user_id')
        variant_id = data.get('variant_id')
        quantity = data.get('quantity', 1)

        if not user_id or not variant_id:
            return jsonify({"error": "user_id and variant_id required"}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT p.price
            FROM product_variant v
            JOIN product p ON v.p_id = p.p_id
            WHERE v.variant_id = %s
        """, (variant_id,))

        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Invalid variant"}), 400

        price = result[0]
        total_price = price * quantity

        cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if cart:
            cart_id = cart[0]
        else:
            cursor.execute("""
                INSERT INTO cart (user_id, created_on, total_items, total_price)
                VALUES (%s, NOW(), 0, 0)
            """, (user_id,))
            cart_id = cursor.lastrowid

        cursor.execute("""
            SELECT quantity FROM cart_items
            WHERE cart_id = %s AND variant_id = %s
        """, (cart_id, variant_id))

        item = cursor.fetchone()

        if item:
            cursor.execute("""
                UPDATE cart_items
                SET quantity = quantity + %s
                WHERE cart_id = %s AND variant_id = %s
            """, (quantity, cart_id, variant_id))
        else:
            cursor.execute("""
                INSERT INTO cart_items (cart_id, variant_id, quantity)
                VALUES (%s, %s, %s)
            """, (cart_id, variant_id, quantity))

        cursor.execute("""
            UPDATE cart
            SET total_items = total_items + %s,
                total_price = total_price + %s
            WHERE cart_id = %s
        """, (quantity, total_price, cart_id))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"message": "Added to cart"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    print("Server running...")
    app.run(debug=True)