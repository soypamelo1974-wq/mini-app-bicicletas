from flask import Flask, jsonify, request, session
import mysql.connector
from practica import to_product  # tu módulo

app = Flask(__name__)
app.secret_key = "supersecret"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_password",
        database="miniapp_db"
    )

@app.route("/api/products", methods=["GET"])
def list_products():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    con = get_db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    con.close()
    return jsonify([to_product(row) for row in rows])
