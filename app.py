from flask import Flask
from flask_jwt_extended import JWTManager
from config.db import db
from models.pet_model import Pet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db.init_app(app)
jwt = JWTManager(app)

# ✅ Register auth routes
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)

# ✅ Register pet routes (MOVE HERE)
from routes.pet_routes import pet_bp
app.register_blueprint(pet_bp)

@app.route('/')
def home():
    return {"message": "API is running successfully"}

from models.user_model import User
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)