from flask import request, current_app, Blueprint
from http import HTTPStatus

from flask.wrappers import Response
from app.models.user_model import UserModel
from flask_jwt_extended import jwt_required
from app.serializer.users_schema import UsersSchema
from app.services.user_services import Userservices



bp_user = Blueprint("bp_user", __name__, url_prefix="/users")


@bp_user.route("/", methods=["GET"])
@jwt_required()
def list_users():
    session = current_app.db.session
    return Userservices(session).get_user_all()

@bp_user.route("/<int:id>", methods=["GET"])
@jwt_required()
def users(id):
    session = current_app.db.session
    return Userservices(session).get_user(id)

@bp_user.route("/register", methods=["POST"])
def create_user():
    session = current_app.db.session
    return Userservices(session).post_create_user(request)

@bp_user.route("/login", methods=["POST"])
def login_user():
    session = current_app.db.session
    return Userservices(session).post_login_user(request)

@bp_user.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    session = current_app.db.session
    return Userservices(session).delete_user(id)

@bp_user.route("/edit/<int:id>", methods=["PUT"])
@jwt_required()
def edit_user(id):
    session = current_app.db.session
    return Userservices(session).put_edit_user(id,request)

@bp_user.route("/edit/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_user(id):
    session = current_app.db.session
    return Userservices(session).patch_user(id,request)
