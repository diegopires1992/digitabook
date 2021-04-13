from flask import request, current_app, Blueprint
from http import HTTPStatus
from app.models.user_model import UserModel


bp_user = Blueprint("bp_user", __name__, url_prefix="/users")

@bp_user.route("/<int:id>", methods=["GET"])
def list_users(id):
    session = current_app.db.session

    found_user: UserModel = UserModel.query.get(id)

    print(found_user.__dict__)

    return {"user": found_user.name}

@bp_user.route("/register", methods=["POST"])
def create_user():
    session = current_app.db.session

    data = request.get_json()
    profile = UserModel(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        cpf=data["cpf"],
        phone=data["phone"],
    )

    session.add(profile)
    session.commit()

    # serializer = BandProfileSerializer(data['band_id'])

    return "user created"