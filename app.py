import firebase_admin
from firebase_admin import credentials
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Firebase connection
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = os.getenv("DB_PASSWORD"),
    database="project_dbms"
)
# -------------------------------
# API 1: Store or Update User
# -------------------------------
@app.route('/store_user', methods=['POST'])
def store_user():
    data = request.get_json(force=True)
    print("STORE USER HIT")
    print(data) 

    uid = data.get('uid')
    name = data.get('name')
    email = data.get('email')
    country_code = data.get('country_code')
    phone_number = data.get('phone_number')

    if not uid or not email:
        return jsonify({"error": "Missing data"}), 400

    cursor = db.cursor()

    cursor.execute("SELECT user_id FROM user WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE user
            SET firebase_uid = %s, name = %s
            WHERE email = %s
        """, (uid, name, email))
    else:
        cursor.execute("""
            INSERT INTO user (name, email, firebase_uid)
            VALUES (%s, %s, %s)
        """, (name, email, uid))

    db.commit()

    return jsonify({"message": "User synced successfully"})


# -------------------------------
# API 2: Get User by UID
# -------------------------------
@app.route('/get_user/<uid>', methods=['GET'])
def get_user(uid):
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, name, email, country_code, phone_number
        FROM user
        WHERE firebase_uid = %s
    """, (uid,))

    user = cursor.fetchone()

    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404
    

    

# GETTING PRODUCT
@app.route('/get_products', methods=['GET'])
def get_products():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.p_id, p.p_name, p.price,
               v.variant_id, v.size_id, v.color_id, v.stock_qty
        FROM product p
        LEFT JOIN product_variant v ON p.p_id = v.p_id
    """)

    rows = cursor.fetchall()

    # Group variants under each product
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

#GET PRODUCTS BY ID
@app.route('/get_product/<p_id>', methods=['GET'])
def get_product(p_id):
    cursor = db.cursor(dictionary=True)

    # Get product
    cursor.execute("""
        SELECT p_id, p_name, description, price
        FROM product
        WHERE p_id = %s
    """, (p_id,))
    
    product = cursor.fetchone()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Get variants
    cursor.execute("""
        SELECT 
    pv.variant_id,
    s.size_label,      
    c.color_name,    
    pv.stock_qty
    FROM product_variant pv
    JOIN size s ON pv.size_id = s.size_id
    JOIN color c ON pv.color_id = c.color_id
    WHERE pv.p_id = %s
    """, (p_id,))

    variants = cursor.fetchall()

    product["variants"] = variants

    return jsonify(product)

# GET PRODUCT BY CATEGORY
@app.route('/get_products_by_category/<category>', methods=['GET'])
def get_products_by_category(category):
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.p_id, p.p_name, p.price,
               v.variant_id, v.size_id, v.color_id, v.stock_qty
        FROM product p
        LEFT JOIN product_variant v ON p.p_id = v.p_id
        WHERE p.category = %s
    """, (category,))

    rows = cursor.fetchall()

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

#SEARCH API
@app.route('/search/<query>', methods=['GET'])
def search_products(query):
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

    return jsonify(cursor.fetchall())

# -------------------------------
# FILTER API
# -------------------------------
@app.route('/filter', methods=['GET'])
def filter_products():
    try:
        query = request.args.get('query')
        category = request.args.get('category')
        min_price = request.args.get('min')
        max_price = request.args.get('max')
        color_id = request.args.get('color_id')
        size_id = request.args.get('size_id')

        # 🆕 Pagination
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))

        # 🆕 Sorting
        sort = request.args.get('sort')

        cursor = db.cursor(dictionary=True)

        sql = """
            SELECT DISTINCT p.p_id, p.p_name, p.price
            FROM product p
            JOIN product_variant v ON p.p_id = v.p_id
            WHERE 1=1
        """

        values = []

        # 🔍 SEARCH
        if query:
            words = query.split()
            conditions = []

            for word in words:
                conditions.append("(p.p_name LIKE %s OR p.description LIKE %s)")
                values.append(f"%{word}%")
                values.append(f"%{word}%")

            sql += " AND (" + " OR ".join(conditions) + ")"

        # 📂 CATEGORY
        if category:
            sql += " AND p.category = %s"
            values.append(category)

        # 💰 PRICE
        if min_price and max_price:
            sql += " AND p.price BETWEEN %s AND %s"
            values.extend([min_price, max_price])

        # 🎨 COLOR
        if color_id:
            sql += " AND v.color_id = %s"
            values.append(color_id)

        # 📏 SIZE
        if size_id:
            sql += " AND v.size_id = %s"
            values.append(size_id)

        # 🔽 SORTING
        if sort == "price_asc":
            sql += " ORDER BY p.price ASC"
        elif sort == "price_desc":
            sql += " ORDER BY p.price DESC"

        # 📄 PAGINATION
        sql += " LIMIT %s OFFSET %s"
        values.extend([limit, offset])

        cursor.execute(sql, values)

        return jsonify(cursor.fetchall())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
#cart
# -------------------------------
# add to cart
import mysql.connector

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        import mysql.connector

        data = request.json

        user_id = data.get('user_id')
        variant_id = data.get('variant_id')
        quantity = data.get('quantity')

        print("DATA RECEIVED:", data)

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password = os.getenv("DB_PASSWORD"),
            database="project_dbms"
        )

        cursor = conn.cursor()

        # ✅ STEP 1: CHECK IF CART EXISTS
        cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if cart:
            cart_id = cart[0]
        else:
            # ✅ CREATE NEW CART
            cursor.execute("""
                INSERT INTO cart (user_id, total_price)
                VALUES (%s, 0)
            """, (user_id,))
            conn.commit()

            cart_id = cursor.lastrowid

        # ✅ STEP 2: INSERT INTO CART_ITEMS
        cursor.execute("""
            INSERT INTO cart_items (cart_id, variant_id, quantity)
            VALUES (%s, %s, %s)
        """, (cart_id, variant_id, quantity))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_cart/<int:user_id>')
def get_cart(user_id):
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password = os.getenv("DB_PASSWORD"),
            database="project_dbms"
        )

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
            ci.variant_id,
            ci.quantity,
            p.price,
            p.p_name,
            s.size_label,
            c.color_name
        FROM cart c1
        JOIN cart_items ci ON c1.cart_id = ci.cart_id
        JOIN product_variant pv ON ci.variant_id = pv.variant_id
        JOIN product p ON pv.p_id = p.p_id
        JOIN size s ON pv.size_id = s.size_id
        JOIN color c ON pv.color_id = c.color_id
        WHERE c1.user_id = %s


        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
    

# update remove from cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    try:
        data = request.json

        cart_id = data.get('cart_id')
        variant_id = data.get('variant_id')

        # 🔴 VALIDATION
        if not cart_id or not variant_id:
            return jsonify({"error": "cart_id and variant_id are required"}), 400

        cursor = db.cursor()

        # Get quantity + price
        cursor.execute("""
            SELECT ci.quantity, p.price
            FROM cart_items ci
            JOIN product_variant v ON ci.variant_id = v.variant_id
            JOIN product p ON v.p_id = p.p_id
            WHERE ci.cart_id = %s AND ci.variant_id = %s
        """, (cart_id, variant_id))

        item = cursor.fetchone()

        if not item:
            return jsonify({"error": "Item not found in cart"}), 404

        qty, price = item
        total_remove_price = qty * price

        # Delete item
        cursor.execute("""
            DELETE FROM cart_items
            WHERE cart_id = %s AND variant_id = %s
        """, (cart_id, variant_id))

        # Update totals
        cursor.execute("""
            UPDATE cart
            SET total_items = total_items - %s,
                total_price = total_price - %s
            WHERE cart_id = %s
        """, (qty, total_remove_price, cart_id))

        db.commit()

        return jsonify({"message": "Item removed"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# REVIEW
# -------------------------------
# ADD REVIEW
@app.route('/add_review', methods=['POST'])
def add_review():
    try:
        data = request.json

        user_id = data.get('user_id')
        p_id = data.get('p_id')
        rating = data.get('rating')
        review_text = data.get('review_text')

        # 🔴 VALIDATION
        if not user_id or not p_id or rating is None:
            return jsonify({"error": "user_id, p_id and rating are required"}), 400

        if rating < 0 or rating > 5:
            return jsonify({"error": "Rating must be between 0 and 5"}), 400

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO review (user_id, p_id, rating, review_text, review_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (user_id, p_id, rating, review_text))

        db.commit()

        return jsonify({"message": "Review added"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#SHOW REVIEW
@app.route('/get_reviews/<p_id>', methods=['GET'])
def get_reviews(p_id):
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, rating, review_text, review_date
        FROM review
        WHERE p_id = %s
        ORDER BY review_date DESC
    """, (p_id,))

    return jsonify(cursor.fetchall())


# SHOW RATING
@app.route('/get_rating/<p_id>', methods=['GET'])
def get_rating(p_id):
    cursor = db.cursor()

    cursor.execute("""
        SELECT ROUND(AVG(rating), 1)
        FROM review
        WHERE p_id = %s
    """, (p_id,))

    avg = cursor.fetchone()[0]

    return jsonify({"average_rating": avg})

#REVIEW COUNT
@app.route('/get_review_count/<p_id>', methods=['GET'])
def get_review_count(p_id):
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM review
        WHERE p_id = %s
    """, (p_id,))

    count = cursor.fetchone()[0]

    return jsonify({"review_count": count})

# -------------------------------
# ML API
# -------------------------------
#Recom based on last bought
@app.route('/recommend/<user_id>', methods=['GET'])
def recommend(user_id):
    cursor = db.cursor(dictionary=True)

    # Step 1: Get last purchased/viewed product
    cursor.execute("""
        SELECT p.category
        FROM cart c
        JOIN cart_items ci ON c.cart_id = ci.cart_id
        JOIN product_variant v ON ci.variant_id = v.variant_id
        JOIN product p ON v.p_id = p.p_id
        WHERE c.user_id = %s
        ORDER BY c.created_on DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "No recommendations yet"})

    category = result['category']

    # Step 2: Recommend similar products
    cursor.execute("""
        SELECT p_id, p_name, price
        FROM product
        WHERE category = %s
        LIMIT 5
    """, (category,))

    return jsonify(cursor.fetchall())

# Seasonal discounts
from datetime import datetime

@app.route('/discount/<p_id>', methods=['GET'])
def seasonal_discount(p_id):
    cursor = db.cursor(dictionary=True)

    # Get product
    cursor.execute("SELECT p_name, price FROM product WHERE p_id = %s", (p_id,))
    product = cursor.fetchone()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    price = product['price']

    month = datetime.now().month

    # 🎯 Simple logic
    if month in [11, 12]:  # winter sale
        discount = 0.20
    elif month in [6, 7]:  # summer sale
        discount = 0.15
    else:
        discount = 0.05

    final_price = int(price * (1 - discount))

    return jsonify({
        "original_price": price,
        "discount": f"{int(discount*100)}%",
        "final_price": final_price
    })

# Price variation on demand
@app.route('/dynamic_price/<p_id>', methods=['GET'])
def dynamic_price(p_id):
    cursor = db.cursor()

    # Count how many times product is in cart
    cursor.execute("""
        SELECT COUNT(*)
        FROM cart_items ci
        JOIN product_variant v ON ci.variant_id = v.variant_id
        WHERE v.p_id = %s
    """, (p_id,))

    demand = cursor.fetchone()[0]

    # Get base price
    cursor.execute("SELECT price FROM product WHERE p_id = %s", (p_id,))
    price = cursor.fetchone()[0]

    # 🎯 Logic
    if demand > 10:
        new_price = int(price * 1.1)  # increase
    elif demand < 3:
        new_price = int(price * 0.9)  # decrease
    else:
        new_price = price

    return jsonify({
        "original_price": price,
        "demand": demand,
        "dynamic_price": new_price
    })

# -------------------------------
# Test Route
# -------------------------------
@app.route('/')
def home():
    return "Backend Running 🚀"


@app.route('/test_insert')
def test_insert():
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO user (name, email, firebase_uid)
        VALUES ('Test User', 'test@gmail.com', 'uid123')
        ON DUPLICATE KEY UPDATE name='Test User'
    """)
    db.commit()
    return "Inserted / Updated Successfully"


# Run server
app.run(host="0.0.0.0", port=5000, debug=True)

