from flask import request, current_app, Blueprint
from http import HTTPStatus

from flask.wrappers import Response
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta


bp_user = Blueprint("bp_user", __name__, url_prefix="/users")

@bp_user.route("/<int:id>", methods=["GET"])
@jwt_required()
def list_users(id):
    try:
        found_user: UserModel = UserModel.query.get_or_404(id)

        return {"user": found_user.name,
                "email": found_user.email}
    except Exception:
        return "Usuario não encontrado",HTTPStatus.BAD_REQUEST

@bp_user.route("/register", methods=["POST"])
def create_user():
    try:        
        session = current_app.db.session

        body = request.get_json()
        email = body.get("email") 

        if not body:
            return {"mensagem":"Verifique o body da resquição"},HTTPStatus.BAD_REQUEST

        found_user: UserModel = UserModel.query.filter_by(email=email).first()
        if found_user:
            return {"mensagem":"Usuario já cadastrado"},HTTPStatus.BAD_REQUEST

        profile = UserModel(
            name=body["name"],
            email=body["email"],
            cpf=body["cpf"],
            phone=body["phone"],
        )

        profile.password = body["password"]

        session.add(profile)
        session.commit()

        return {"user": profile.name, "email": profile.email},HTTPStatus.CREATED

    except Exception:
        return "Erro ao Cadastrar",HTTPStatus.BAD_REQUEST

@bp_user.route("/login", methods=["POST"])
def login_user():
    try:
        body = request.get_json()

        email = body.get("email")
        password = body.get("password")

        found_user:UserModel = UserModel.query.filter_by(email = email).first()

        if not found_user or not found_user.check_password(password):
            return {"msg": "Usuario ou senha incorretos"}, HTTPStatus.NOT_FOUND

        access_token = create_access_token(identity=found_user.id,expires_delta=timedelta(days=7))

        return {"token": access_token}

    except Exception:
        return "Erro no Login",HTTPStatus.BAD_REQUEST


@bp_user.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    session = current_app.db.session

    found_user: UserModel = UserModel.query.get_or_404(id)

    session.delete(found_user)
    session.commit()

    return "usuario deletado",HTTPStatus.NO_CONTENT


@bp_user.route("/edit/<int:id>", methods=["PUT"])
@jwt_required()
def edit_user(id):
    try:
        session = current_app.db.session
        body = request.get_json()
        edited_profile: UserModel = UserModel.query.get_or_404(id)
      
        edited_profile.name = body.get("name")
        edited_profile.email = body.get("email")
        edited_profile.cpf = body.get("cpf")
        edited_profile.phone = body.get("phone")
        edited_profile.password = body.get("password")

        session.add(edited_profile)
        session.commit()
            
        return {"user": edited_profile.name, "email": edited_profile.email},HTTPStatus.OK
    except Exception as a :        
        return "Erro informações utilizadas anteriormente não podem ser utilizadas",HTTPStatus.BAD_REQUEST


@bp_user.route("/edit/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_user(id):

    try:
        session = current_app.db.session
        found_user: UserModel = UserModel.query.get(id)
        body = request.get_json()

        response = []
    
        for key, value in body.items():            
            response.append(key)
            setattr(found_user, key, value)
    
        change_info = ','.join([str(elem) for elem in response])

        session.add(found_user)
        session.commit()

        return {"campos_alterados":change_info},HTTPStatus.OK
    except Exception:
        return "Erro ao alterar o Usuario",HTTPStatus.BAD_REQUEST