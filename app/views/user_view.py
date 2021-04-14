from flask import request, current_app, Blueprint
from http import HTTPStatus
from app.models.user_model import UserModel


bp_user = Blueprint("bp_user", __name__, url_prefix="/users")

@bp_user.route("/<int:id>", methods=["GET"])
def list_users(id):
    session = current_app.db.session

    found_user: UserModel = UserModel.query.get(id)

    print(found_user.__dict__)

    return {"user": found_user.name,
            "email": found_user.email}

@bp_user.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    session = current_app.db.session

    found_user: UserModel = UserModel.query.get_or_404(id)

    print(found_user.__dict__)

    session.delete(found_user)
    session.commit()

    return "usuario deletado",HTTPStatus.NO_CONTENT


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

    return "user logado"    


@bp_user.route("/edit/<int:id>", methods=["PUT"])
def edit_user(id):

    session = current_app.db.session
    
    data = request.get_json()
    edited_profile: UserModel = UserModel.query.get_or_404(id)
    
    
    edited_profile.name = data["name"]
    edited_profile.email = data["email"]
    edited_profile.cpf = data["cpf"]
    edited_profile.phone = data["phone"]
    edited_profile.password = data["password"]
    
    print(data)

    session.add(edited_profile)
    session.commit()

        
    return {"user": edited_profile.name, "email": edited_profile.email},HTTPStatus.OK


@bp_user.route("/edit/<int:id>", methods=["PATCH"])
def patch_user(id):

    session = current_app.db.session
    found_user: UserModel = UserModel.query.get(id)
    data = request.get_json()

    try:
        for key, value in data.items():
            setattr(found_user, key, value)
        session.add(found_user)
        session.commit()

        return {"user": found_user.name, "email": found_user.email},HTTPStatus.OK
    except Exception as nome:
        return "test",HTTPStatus.BAD_REQUEST
           
    
