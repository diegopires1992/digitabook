from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from app.models.authors_model import AuthorModel
from json import dumps

bp_authors = Blueprint('bp_authors', __name__, url_prefix='/author')


@bp_authors.route('/', methods=["GET"])
def get_authors():
    session = current_app.db.session

    authors = [
        {
            "id": author.id,
            "name": author.name,
            "birthplace": author.birthplace
        }

        for author in session.query(AuthorModel).all()
    ]

    return jsonify(authors), HTTPStatus.OK


@bp_authors.route('/', methods=["POST"])
def create_author():
    session = current_app.db.session

    body = request.get_json()

    name = body.get('name')
    birthplace = body.get('birthplace')

    new_author = AuthorModel(name=name, birthplace=birthplace)
    session.add(new_author)
    session.commit()

    return {
        "author": {
            "id": new_author.id,
            "name": new_author.name,
            "birthplace": new_author.birthplace
        }
    }
