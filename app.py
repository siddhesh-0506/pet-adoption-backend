from flask import Flask
from flask_jwt_extended import JWTManager
from config.db import db
import os

print("APP STARTING...")

app = Flask(__name__)

# ✅ Use environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///test.db")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
jwt = JWTManager(app)

# ✅ Register routes
from routes.auth_routes import auth_bp
from routes.pet_routes import pet_bp

app.register_blueprint(auth_bp)
app.register_blueprint(pet_bp)

@app.route('/')
def home():
    return {"message": "API is running successfully"}

# ✅ Create DB tables
from models.user_model import User
from models.pet_model import Pet

with app.app_context():
    db.create_all()

# ❌ REMOVE debug=True
if __name__ == '__main__':
    app.run()