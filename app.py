import os
from flask import Flask, render_template
from config import Config
from models import db
from routes.api import api_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
