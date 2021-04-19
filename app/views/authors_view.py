from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from app.models.authors_model import AuthorModel

bp_authors = Blueprint('bp_authors', __name__, url_prefix='/author')


@bp_authors.route('/', methods=["GET"])
def get_authors():
    authors = [
        {
            "id": author.id,
            "name": author.name,
            "birthplace": author.birthplace
        }

        for author in AuthorModel.query.all()
    ]

    return {
        "authors": authors
    }, HTTPStatus.OK


@bp_authors.route('/', methods=["POST"])
def create_author():
    session = current_app.db.session

    try:

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

    except Exception:
        return {"message": "error when registering"}, HTTPStatus.BAD_REQUEST


@bp_authors.route("/<int:id>", methods=["GET"])
def get_author_by_id(id):
    authors_id = id

    try:

        found_author = AuthorModel.query.get(id)

        return {
            "author": {
                "id": found_author.id,
                "name": found_author.name,
                "birthplace": found_author.birthplace
            }
        }
    except Exception:
        return {"message": "author not found"}, HTTPStatus.BAD_REQUEST


@bp_authors.route("/<int:id>", methods=["DELETE"])
def delete_author(id):
    session = current_app.db.session

    author_id = id

    try:

        found_author = AuthorModel.query.get(id)

        session.delete(found_author)
        session.commit()

        return {"message": "deleted author"}, HTTPStatus.NO_CONTENT
    except Exception:
        return {"message": "author not found"}, HTTPStatus.BAD_REQUEST
