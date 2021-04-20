from . import (
    Flask,
    UsersSchema,
    UserModel,
    HTTPStatus
)
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta


class Userservices:
    def __init__(self, session):
        self.session = session

    def get_user_all(self):
        try:
            users = UserModel.query.all()

            users_list = UsersSchema(many=True).dump(users)

            return {'users': users_list}, HTTPStatus.OK
        except Exception:
            return "Falha ao pegar os usuarios", HTTPStatus.BAD_REQUEST

    def get_user(self, id):
        try:
            user: UserModel = UserModel.query.get(id)
            if not user:
                return "Usuario não encontrado", HTTPStatus.BAD_REQUEST

            return {"user": UsersSchema().dump(user)}, HTTPStatus.OK
        except Exception:
            return "Falha ao pegar o usuario", HTTPStatus.BAD_REQUEST

    def post_create_user(self, request):
        try:
            body = request.get_json()
            email = body.get("email")

            if not body:
                return {"mensagem": "Verifique o body da resquição"}, HTTPStatus.BAD_REQUEST

            found_user: UserModel = UserModel.query.filter_by(
                email=email).first()
            if found_user:
                return {"mensagem": "Usuario já cadastrado"}, HTTPStatus.BAD_REQUEST

            profile = UserModel(
                name=body["name"],
                email=body["email"],
                cpf=body["cpf"],
                phone=body["phone"],
            )

            profile.password = body["password"]

            self.session.add(profile)
            self.session.commit()
            user_create: UserModel = UserModel.query.get(profile.id)
            return {"user": UsersSchema().dump(user_create)}, HTTPStatus.CREATED

        except Exception:
            return "Erro ao Cadastrar", HTTPStatus.BAD_REQUEST

    def post_login_user(self, request):
        try:
            body = request.get_json()

            email = body.get("email")
            password = body.get("password")

            found_user: UserModel = UserModel.query.filter_by(
                email=email).first()

            if not found_user or not found_user.check_password(password):
                return {"msg": "Usuario ou senha incorretos"}, HTTPStatus.NOT_FOUND

            access_token = create_access_token(
                identity=found_user.id, expires_delta=timedelta(days=7))

            return {"token": access_token}

        except Exception:
            return "Erro no Login", HTTPStatus.BAD_REQUEST

    def delete_user(self, id):
        try:
            found_user: UserModel = UserModel.query.get_or_404(id)

            self.session.delete(found_user)
            self.session.commit()

            return "usuario deletado", HTTPStatus.NO_CONTENT
        except Exception:
            return "Erro a deletar usuario", HTTPStatus.BAD_REQUEST

    def put_edit_user(self, id, request):
        try:
            body = request.get_json()
            edited_profile: UserModel = UserModel.query.get_or_404(id)

            edited_profile.name = body.get("name")
            edited_profile.email = body.get("email")
            edited_profile.cpf = body.get("cpf")
            edited_profile.phone = body.get("phone")
            edited_profile.password = body.get("password")

            self.session.add(edited_profile)
            self.session.commit()

            return {"user": UsersSchema().dump(edited_profile)}, HTTPStatus.OK
        except Exception:
            return "Erro ao editar", HTTPStatus.BAD_REQUEST

    def patch_user(self, id, request):
        try:
            found_user: UserModel = UserModel.query.get(id)
            body = request.get_json()
            if not body:
                return {"mensagem": "Verifique o body da resquição"}, HTTPStatus.BAD_REQUEST

            for key, value in body.items():
                setattr(found_user, key, value)

            self.session.add(found_user)
            self.session.commit()
            return "User alterado", HTTPStatus.OK

        except Exception:
            return "Erro ao alterar o Usuario", HTTPStatus.BAD_REQUEST
