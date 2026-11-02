import mysql.connector
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="surabhi2004",
        database="OnlineShopping"
    )

@app.route("/")
def home():
    db = get_db_connection()
    cursor = db.cursor()

    # 1. Total Customers
    cursor.execute("SELECT COUNT(*) FROM Customers")
    customers_count = cursor.fetchone()[0]

    # 2. Total Products
    cursor.execute("SELECT COUNT(*) FROM Products")
    products_count = cursor.fetchone()[0]

    # 3. Total Orders
    cursor.execute("SELECT COUNT(*) FROM Orders")
    orders_count = cursor.fetchone()[0]

    # 4. Recent Orders
    cursor.execute("""
        SELECT Customers.name, Orders.order_id,
        Orders.order_date, Orders.total_amount
        FROM Customers
        INNER JOIN Orders
        ON Customers.customer_id = Orders.customer_id
        ORDER BY Orders.order_id DESC
    """)
    recent_orders = cursor.fetchall()

    # 5. Total Revenue
    cursor.execute("SELECT SUM(total_amount) FROM Orders")
    revenue = cursor.fetchone()[0] or 0

    # 6. Payment Report
    cursor.execute("""
        SELECT payment_status, COUNT(*)
        FROM Payments
        GROUP BY payment_status
    """)
    payment_report = cursor.fetchall()

    # 7. Products List
    cursor.execute("""
        SELECT product_id, product_name, category, price, stock
        FROM Products
    """)
    product_list = cursor.fetchall()

    # 8. Customers List
    cursor.execute("""
        SELECT customer_id, name, email, phone, address
        FROM Customers
    """)
    customer_list = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        customers=customers_count,
        products=products_count,
        orders=orders_count,
        recent_orders=recent_orders,
        revenue=revenue,
        payment_report=payment_report,
        product_list=product_list,
        customer_list=customer_list
    )


@app.route("/add_product", methods=["POST"])
def add_product():
    db = get_db_connection()
    cursor = db.cursor()

    product_name = request.form["product_name"]
    category = request.form["category"]
    price = request.form["price"]
    stock = request.form["stock"]

    sql = """
        INSERT INTO Products (product_name, category, price, stock)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (product_name, category, price, stock))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")
# Add Customer Route
@app.route("/add_customer", methods=["POST"])
def add_customer():
    db = get_db_connection()
    cursor = db.cursor()

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]

    cursor.execute("""
        INSERT INTO Customers (name, email, phone, address)
        VALUES (%s, %s, %s, %s)
    """, (name, email, phone, address))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
