from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import re

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto
app.config.from_object('config.Config')

# Configuración MySQL
mysql = MySQL(app)

# Carpeta para guardar imágenes
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------------------
# Funciones auxiliares
# ----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != role:
                flash('No tienes permisos para acceder a esta página.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------------
# Rutas de usuario
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        password = request.form['password'].strip()

        # Validaciones
        if not username or not email or not phone or not password:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return redirect(url_for('register'))
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('El correo electrónico no es válido.', 'danger')
            return redirect(url_for('register'))
        if not re.match(r"^[0-9]{10}$", phone):
            flash('El número de teléfono debe tener 10 dígitos.', 'danger')
            return redirect(url_for('register'))

        cur = mysql.connection.cursor()
        # Verificar duplicados
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            cur.close()
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('register'))
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            cur.close()
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('register'))

        # Guardar usuario
        hashed_password = generate_password_hash(password)
        cur.execute("""
            INSERT INTO users (username, email, phone, password)
            VALUES (%s, %s, %s, %s)
        """, (username, email, phone, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not email or not password:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['logged_in'] = True
            session['username'] = user[1]  # seguimos guardando el username en sesión
            session['role'] = user[3]
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado la sesión.', 'info')
    return redirect(url_for('index'))

# ----------------------------
# Dashboard
# ----------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()

    if session['role'] == 'admin':
        return render_template('dashboard_admin.html', products=products)
    else:
        return render_template('dashboard_client.html', products=products)

# ----------------------------
# CRUD Productos (Admin)
# ----------------------------
@app.route('/admin/products/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        file = request.files.get('image_file')

        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f'/static/uploads/{filename}'

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO products (name, description, price, stock, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, price, stock, image_url))
        mysql.connection.commit()
        cur.close()
        flash('Producto creado con éxito.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_product.html')

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_product(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        file = request.files.get('image_file')

        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f'/static/uploads/{filename}'

        if image_url:
            cur.execute("""
                UPDATE products SET name=%s, description=%s, price=%s, stock=%s, image_url=%s WHERE id=%s
            """, (name, description, price, stock, image_url, id))
        else:
            cur.execute("""
                UPDATE products SET name=%s, description=%s, price=%s, stock=%s WHERE id=%s
            """, (name, description, price, stock, id))

        mysql.connection.commit()
        cur.close()
        flash('Producto actualizado con éxito.', 'success')
        return redirect(url_for('dashboard'))

    cur.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cur.fetchone()
    cur.close()
    return render_template('edit_product.html', product=product)

@app.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado con éxito.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'logged_in' not in session or session.get('role') != 'cliente':
        flash("Debes iniciar sesión como cliente para agregar al carrito.", "warning")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if not product or product[4] <= 0:
        flash("Producto no disponible.", "danger")
        return redirect(url_for('dashboard'))

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product[1],
            'price': float(product[3]),
            'quantity': 1
        }

    session['cart'] = cart
    flash(f"{product[1]} se agregó al carrito.", "success")
    return redirect(url_for('dashboard'))
# ----------------------------
# Ejecutar la app
# ----------------------------
if __name__ == '__main__':
    # Crear carpeta uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
