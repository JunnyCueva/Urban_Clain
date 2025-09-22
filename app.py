from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

# Esquema de la base de datos (Ejemplo en SQL)
# Ejecuta este SQL en tu base de datos MySQL antes de iniciar la aplicación.
# CREATE DATABASE tienda_ropa;
# USE tienda_ropa;
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) NOT NULL UNIQUE,
#     password VARCHAR(255) NOT NULL,
#     role ENUM('cliente', 'admin') DEFAULT 'cliente'
# );

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar que los campos no estén vacíos
        if not username or not password:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'El nombre de usuario "{username}" ya existe. Por favor, elige otro.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar que los campos no estén vacíos
        if not username or not password:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['logged_in'] = True
            session['username'] = user[1]
            session['role'] = user[3]
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))
    
    products = []  # Inicializa la lista de productos como vacía
    if session['role'] == 'admin':
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
            cur.close()
        except Exception as e:
            flash(f"Error al cargar productos: {e}", "danger")

    return render_template('dashboard.html', role=session['role'], products=products)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado la sesión.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)