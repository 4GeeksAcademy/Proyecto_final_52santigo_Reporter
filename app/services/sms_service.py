from twilio.rest import Client
import os

# Servicio real de envío de SMS usando Twilio
def send_sms(phone_number, message):
    try:
        # Credenciales de Twilio desde el archivo .env
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

        # Crear cliente de Twilio
        client = Client(account_sid, auth_token)

        # Enviar el mensaje
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message,
            to=phone_number
        )

        print(f"Mensaje enviado exitosamente con SID: {message.sid}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        raise
