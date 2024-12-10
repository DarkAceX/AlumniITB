from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de base de datos de usuarios (esto debería ser reemplazado por una base de datos real)
users = {"egresado@itb.edu.ec": "password123"}

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Verifica si el usuario existe y la contraseña es correcta
    if users.get(username) == password:
        return redirect(url_for('dashboard'))  # Redirige al área de miembros
    else:
        return render_template('main.html', error="Credenciales incorrectas")

@app.route('/dashboard')
def dashboard():
    return "Bienvenido al área de miembros"

