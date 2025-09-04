import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Base pour SQLAlchemy
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Créer l'application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")  # clé par défaut en local
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # utile pour Render (HTTPS)

# Config de la base de données (Render fournit DATABASE_URL)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialiser l’extension
db.init_app(app)

with app.app_context():
    import models  # importe les modèles pour créer les tables
    db.create_all()
    logging.info("✅ Tables de la base créées avec succès.")

# Route principale
@app.route("/")
def home():
    return "Bienvenue sur Health Assistant 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
