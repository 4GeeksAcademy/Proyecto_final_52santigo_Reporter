from flask import Flask, request, jsonify, abort
from flasgger import Swagger
from app import create_app, db
from app.models import User, Task
from twilio.rest import Client
import threading
import time
import os

# Crear la aplicación Flask
app = create_app()

# Configurar Swagger con categorías organizadas
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Reporte.IA",
        "description": "API para gestionar usuarios, tareas y mensajes SMS.",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {"name": "Usuarios", "description": "Gestión de usuarios"},
        {"name": "Tareas", "description": "Gestión de tareas y countdown"},
        {"name": "Mensajes", "description": "Gestión y envío de mensajes SMS"},
        {"name": "Default", "description": "Rutas por defecto"}
    ]
})

# Diccionario para manejar los hilos activos
active_timers = {}

# Servicio real de envío de SMS usando Twilio
def send_sms(phone_number, message):
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

        # Crear cliente de Twilio
        client = Client(account_sid, auth_token)

        # Enviar el mensaje
        message_response = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message,
            to=phone_number
        )

        print(f"Mensaje enviado exitosamente con SID: {message_response.sid}")
        return message_response.sid
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        raise

# Función para manejar la cuenta regresiva
def countdown_timer(task_id):
    task = Task.query.get(task_id)
    if not task:
        return
    while task.countdown > 0:
        time.sleep(1)
        task.countdown -= 1
        db.session.commit()
    if task.countdown == 0:
        send_sms(task.user.phone_number, task.message)
        print(f"Mensaje enviado: {task.message}")

# Default: Ruta raíz
@app.route('/')
def home():
    """
    Información general de la API
    ---
    tags:
      - Default
    responses:
      200:
        description: Información del proyecto
        examples:
          application/json: {
            "message": "Bienvenido a la API de Reporte.IA"
          }
    """
    return jsonify({"message": "Bienvenido a la API de Reporte.IA"}), 200

# Usuarios: Crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    """
    Crear un nuevo usuario
    ---
    tags:
      - Usuarios
    """
    data = request.get_json()
    if not data or 'email' not in data or 'username' not in data or 'password' not in data or 'phone_number' not in data:
        abort(400, "Faltan datos requeridos")
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(email=data['email'], username=data['username'], password=hashed_password, phone_number=data['phone_number'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# Mensajes: Enviar mensaje directo
@app.route('/messages', methods=['POST'])
def send_message():
    """
    Enviar un mensaje SMS
    ---
    tags:
      - Mensajes
    """
    data = request.get_json()
    if not data or 'phone_number' not in data or 'message' not in data:
        abort(400, "Faltan datos requeridos (phone_number, message)")
    
    phone_number = data['phone_number']
    message_content = data['message']

    try:
        # Llama a la función para enviar el mensaje
        message_sid = send_sms(phone_number, message_content)
        return jsonify({
            "message": "Mensaje enviado exitosamente",
            "sid": message_sid
        }), 201
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        abort(500, "Error interno al enviar el mensaje")
