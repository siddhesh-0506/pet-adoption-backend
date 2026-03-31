from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.db import db
from models.pet_model import Pet
from config.aws_config import s3, BUCKET_NAME
import uuid

pet_bp = Blueprint('pet', __name__)

# ---------------- ADD PET ----------------
@pet_bp.route('/pets', methods=['POST'])
@jwt_required()
def add_pet():
    data = request.form
    file = request.files.get('image')

    print(request.form)
    print(request.files)


    user_id = get_jwt_identity()

    name = data.get('name')
    age = int(data.get('age')) if data.get('age') else None
    breed = data.get('breed')
    location = data.get('location')

    if not all([name, age, breed, location]):
        return jsonify({"error": "Missing fields"}), 400

    image_url = None

    # 🔥 AWS S3 Upload
    if file:
        file_name = str(uuid.uuid4()) + "_" + file.filename

        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            file_name
        )

        image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"

    pet = Pet(
        name=name,
        age=age,
        breed=breed,
        location=location,
        owner_id=user_id,
        image_url=image_url
    )

    db.session.add(pet)
    db.session.commit()

    return jsonify({
        "message": "Pet added successfully",
        "image_url": image_url
    })


# ---------------- GET ALL PETS ----------------
@pet_bp.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()

    result = []
    for pet in pets:
        result.append({
            "id": pet.id,
            "name": pet.name,
            "age": pet.age,
            "breed": pet.breed,
            "location": pet.location
        })

    return jsonify(result)