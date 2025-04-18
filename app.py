from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
import sqlite3
import os
import subprocess
import requests

app = Flask(__name__)
app.secret_key = 'clave_muy_secreta_y_debil'

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# ------------------- VULNERABILIDAD 1: INYECCIÓN SQL -------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABLE: Construcción directa de consulta SQL con entradas del usuario
        # No se usa parameterización ni sanitización
        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            error = 'Credenciales inválidas. Intente nuevamente.'
    
    return render_template('login.html', error=error)

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    
    # VULNERABLE: Construcción directa de consulta SQL con entradas del usuario
    conn = get_db_connection()
    query = f"SELECT * FROM products WHERE name LIKE '%{keyword}%'"
    
    if category:
        query += f" AND category = '{category}'"
    
    products = conn.execute(query).fetchall()
    conn.close()
    
    return render_template('search_results.html', products=products, keyword=keyword, category=category)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

# ------------------- VULNERABILIDAD 2: INYECCIÓN DE COMANDOS -------------------

@app.route('/network_tool', methods=['GET', 'POST'])
def network_tool():
    output = None
    if request.method == 'POST':
        host = request.form['host']
        
        # VULNERABLE: Ejecución directa de comandos con entrada del usuario
        # Sin validación ni sanitización
        command = f"ping -c 4 {host}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
    
    return render_template('network_tool.html', output=output)

@app.route('/file_reader', methods=['GET', 'POST'])
def file_reader():
    content = None
    error = None
    if request.method == 'POST':
        filename = request.form['filename']
        
        # VULNERABLE: Ejecución directa de comandos para leer archivos
        try:
            command = f"cat {filename}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                content = result.stdout
            else:
                error = f"Error al leer el archivo: {result.stderr}"
        except Exception as e:
            error = f"Excepción: {str(e)}"
    
    return render_template('file_reader.html', content=content, error=error)

# ------------------- VULNERABILIDAD 3: VALIDACIÓN DE ENTRADA INCORRECTA -------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # VULNERABLE: Falta de validación adecuada de entradas
        # No hay verificación de longitud, formato de email, caracteres especiales, etc.
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                         (username, password, email, 'user'))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = 'El nombre de usuario ya existe. Elija otro.'
        finally:
            conn.close()
    
    return render_template('register.html', error=error)

@app.route('/comment/add', methods=['POST'])
def add_comment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    comment_text = request.form['comment']
    
    # VULNERABLE: No hay validación de longitud ni sanitización
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (product_id, username, comment) VALUES (?, ?, ?)',
                 (product_id, session['username'], comment_text))
    conn.commit()
    conn.close()
    
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE product_id = ?', (product_id,)).fetchall()
    conn.close()
    
    if product is None:
        abort(404)
    
    return render_template('product_detail.html', product=product, comments=comments)

# ------------------- VULNERABILIDAD 4: SSRF (SERVER-SIDE REQUEST FORGERY) -------------------

@app.route('/check_website', methods=['GET', 'POST'])
def check_website():
    preview = None
    status = None
    if request.method == 'POST':
        url = request.form['url']
        
        # VULNERABLE: No hay validación de URL ni restricciones
        try:
            response = requests.get(url, timeout=5)
            preview = response.text[:500] + '...' if len(response.text) > 500 else response.text
            status = f"Status Code: {response.status_code}"
        except Exception as e:
            status = f"Error: {str(e)}"
    
    return render_template('check_website.html', preview=preview, status=status)

@app.route('/api/fetch_resource', methods=['GET'])
def fetch_resource():
    resource_url = request.args.get('url', '')
    
    if not resource_url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    # VULNERABLE: No hay validación de URL ni restricciones
    try:
        response = requests.get(resource_url, timeout=5)
        return jsonify({
            'status': response.status_code,
            'content_type': response.headers.get('Content-Type', ''),
            'content': response.text[:1000]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- OTRAS RUTAS -------------------

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        from init_db import init_db
        init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)