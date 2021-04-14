from flask import request, current_app, Blueprint
from http import HTTPStatus
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta


bp_user = Blueprint("bp_user", __name__, url_prefix="/users")

@bp_user.route("/<int:id>", methods=["GET"])
def list_users(id):
    session = current_app.db.session

    found_user: UserModel = UserModel.query.get(id)

    print(found_user.__dict__)

    return {"user": found_user.name,
            "email": found_user.email}

@bp_user.route("/register", methods=["POST"])
def create_user():
    session = current_app.db.session

    data = request.get_json()

    profile = UserModel(
        name=data["name"],
        email=data["email"],
        cpf=data["cpf"],
        phone=data["phone"],
    )

    profile.password = data["password"]

    session.add(profile)
    session.commit()

    return {"user": profile.name, "email": profile.email},HTTPStatus.CREATED

@bp_user.route("/login", methods=["POST"])
def login_user():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    found_user:UserModel = UserModel.query.filter_by(email = email).first()
    
    if not found_user or not found_user.check_password(password):
        return {"msg": "Usuario ou senha incorretos"}, HTTPStatus.NOT_FOUND

    access_token = create_access_token(identity=found_user.id,expires_delta=timedelta(days=7))

    return {"token": access_token}  


@bp_user.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    session = current_app.db.session

    found_user: UserModel = UserModel.query.get_or_404(id)

    print(found_user.__dict__)

    session.delete(found_user)
    session.commit()

    return "usuario deletado",HTTPStatus.NO_CONTENT


@bp_user.route("/edit/<int:id>", methods=["PUT"])
@jwt_required()
def edit_user(id):

    session = current_app.db.session
    try:
        data = request.get_json()
        edited_profile: UserModel = UserModel.query.get_or_404(id)
      
        edited_profile.name = data["name"]
        edited_profile.email = data["email"]
        edited_profile.cpf = data["cpf"]
        edited_profile.phone = data["phone"]
        edited_profile.password = data["password"]

        session.add(edited_profile)
        session.commit()
        return "test2"
            
        return {"user": edited_profile.name, "email": edited_profile.email},HTTPStatus.OK
    except Exception as teste:
        print(teste)
        return "test"


@bp_user.route("/edit/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_user(id):

    session = current_app.db.session
    found_user: UserModel = UserModel.query.get(id)
    data = request.get_json()
    print(data)
    return "teste"
    
    try:
        for key, value in data.items():
            setattr(found_user, key, value)
        session.add(found_user)
        session.commit()

        return {"user": found_user.name, "email": found_user.email},HTTPStatus.OK
    except Exception as nome:
        print(nome)
        return "test",HTTPStatus.BAD_REQUEST