# auth.py
try:
    from flask import (  # pyright: ignore[reportMissingImports]
        Blueprint,
        render_template,
        request,
        redirect,
        url_for,
        session,
    )
except ModuleNotFoundError as error:
    if error.name == "flask":
        raise ModuleNotFoundError(
            "Flask no está instalado. Ejecuta: python -m pip install Flask"
        ) from error
    raise
try:
    from werkzeug.security import (  # pyright: ignore[reportMissingImports]
        generate_password_hash,
        check_password_hash,
    )
except ModuleNotFoundError as error:
    if error.name == "werkzeug":
        raise ModuleNotFoundError(
            "Werkzeug no está instalado. Ejecuta: python -m pip install Werkzeug"
        ) from error
    raise
import mysql.connector  # pyright: ignore[reportMissingImports]

auth = Blueprint('auth', __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_password",
        database="miniapp_db"
    )

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
        con.commit()
        con.close()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = get_db()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        con.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect(url_for('crud.list_items'))
    return render_template('login.html')
