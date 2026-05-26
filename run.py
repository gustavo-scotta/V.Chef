from flask import Flask
from app.controllers.home_controller import home_bp
from app.controllers.despensa_controller import despensa_bp
from app.controllers.preferencias_controller import preferencias_bp

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

app.register_blueprint(home_bp)
app.register_blueprint(despensa_bp)
app.register_blueprint(preferencias_bp)

if __name__ == '__main__':
    app.run(debug=True)