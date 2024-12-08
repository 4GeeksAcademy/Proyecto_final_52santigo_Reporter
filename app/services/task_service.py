from app.models.task_model import Task
from app.services.sms_service import send_sms
from app import db
import threading
import time

def countdown_timer(task):
    while task.countdown > 0:
        time.sleep(1)
        task.countdown -= 1
        print(f"Tarea {task.id} - Tiempo restante: {task.countdown}")
    
    if task.countdown == 0:
        send_sms(task.user.phone_number, task.message)

def create_task(data, user):
    task = Task(**data, user=user)
    db.session.add(task)
    db.session.commit()

    threading.Thread(target=countdown_timer, args=(task,)).start()
    return task
