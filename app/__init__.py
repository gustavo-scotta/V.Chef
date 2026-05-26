from flask import Flask


def create_app():

    app = Flask(__name__)

    from app.controllers.despensa_controller import main
    from app.controllers.home_controller import main
    from app.controllers.preferencias_controller import main
    app.register_blueprint(main)

    return app