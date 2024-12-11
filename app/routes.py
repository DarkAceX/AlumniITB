import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Lista de usuarios para prueba (esto debe estar en una base de datos en un caso real)
USUARIOS = {
    "administrador": "admin12345"
}

# Lista de usuarios registrados (esto también debe estar en una base de datos)
users = {
    "user1": {
        "fullname": "Nombre del usuario",
        "password": "user12345",
        "file_path": "ruta_al_documento",
        "estado": "activo",
        "role": "user"
    }
}

# Página principal
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Verifica si el usuario es administrador
    if username in USUARIOS and USUARIOS[username] == password:
        session['username'] = username  # Guardar en la sesión
        return redirect(url_for('admin'))  # Redirigir al panel de administración
    
    # Si no es administrador, verifica si está en los usuarios comunes
    elif username in users and users[username]['password'] == password:
        session['username'] = username  # Guardar en la sesión
        return redirect(url_for('dashboard'))  # Redirigir al área de miembros
    
    # Si no se encuentra el usuario o las credenciales son incorrectas
    else:
        flash('Credenciales incorrectas', 'danger')
        return redirect(url_for('index'))  # Si las credenciales son incorrectas

# Ruta para registrarse
@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    file = request.files['validation_document']

    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for('index'))

    if username in users:
        flash("El usuario ya está registrado.", "error")
        return redirect(url_for('index'))

    if file:
        filename = f"{username}_{file.filename}"
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Guardar en la "base de datos" como usuario inactivo
        users[username] = {
            "fullname": fullname,
            "password": password,
            "file_path": file_path,
            "estado": "inactivo",
            "role": "user"  # Solo usuarios comunes
        }

        flash("Registro exitoso. Espera la validación del administrador.", "success")
        return redirect(url_for('index'))
    else:
        flash("Debes subir un documento de validación.", "error")
        return redirect(url_for('index'))

# Página del área de miembros
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Debes iniciar sesión primero', 'danger')
        return redirect(url_for('index'))  # Redirige a la página principal si no hay sesión
    
    return "Bienvenido al área de miembros"


# Página de administración
@app.route('/admin')
def admin():
    # Asegúrate de que solo los administradores puedan acceder a esta página
    if 'username' not in session or session['username'] != "administrador":
        flash('No tienes permisos para acceder al panel de administración', 'danger')
        return redirect(url_for('index'))

    # Aquí obtienes los usuarios pendientes para aprobar
    pending_users = [
        (username, user["fullname"], user["file_path"], user["estado"])
        for username, user in users.items()
        if user["role"] == "user" and user["estado"] == "inactivo"
    ]
    
    return render_template('admin.html', pending_users=pending_users)


# Ruta para habilitar un usuario
@app.route('/approve/<username>', methods=['POST'])
def approve_user(username):
    if 'username' not in session or session['username'] != "administrador":
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('index'))
    
    user = users.get(username)
    if user:
        user["estado"] = "activo"  # Cambiar el estado a "activo"
        flash(f"El usuario {username} ha sido habilitado.", "success")
        return redirect(url_for('admin'))
    else:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for('admin'))

# Ruta para rechazar un usuario
@app.route('/reject/<username>', methods=['POST'])
def reject_user(username):
    if 'username' not in session or session['username'] != "administrador":
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('index'))
    
    if username in users:
        del users[username]  # Elimina al usuario de la "base de datos"
        flash(f"El usuario {username} ha sido rechazado.", "success")
        return redirect(url_for('admin'))
    else:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for('admin'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)  # Eliminar la sesión
    return redirect(url_for('index'))  # Redirigir al inicio

if __name__ == '__main__':
    app.run(debug=True)

