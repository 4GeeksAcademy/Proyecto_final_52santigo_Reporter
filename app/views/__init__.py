def register_routes(app):
    from app.views.task_view import task_bp
    from app.views.user_view import user_bp
    # from app.views.ask_view import ask_bp  # Elimina esta línea si no tienes ask_view

    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    # app.register_blueprint(ask_bp)  # Elimina esta línea si no tienes ask_bp
