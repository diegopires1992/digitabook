from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from app.models.authors_model import AuthorModel
from . import AuthorServices

bp_authors = Blueprint('bp_authors', __name__, url_prefix='/authors')


@bp_authors.route('/', methods=["GET"])
def get_authors():
    session = current_app.db.session
    return AuthorServices(session).get_all_authors()


@bp_authors.route('/', methods=["POST"])
def create_author():
    session = current_app.db.session
    return AuthorServices(session).post_create_author(request)


@bp_authors.route("/<int:authors_id>", methods=["GET"])
def get_author_by_id(authors_id):
    session = current_app.db.session
    return AuthorServices(session).get_authors_by_id_service(authors_id)


@bp_authors.route("/<int:authors_id>", methods=["DELETE"])
def delete_author(authors_id):
    session = current_app.db.session
    return AuthorServices(session).delete_author(authors_id)
