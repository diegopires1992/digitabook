from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from app.models.product_model import ProductModel
from app.models.authors_model import AuthorModel
from sqlalchemy import update
from app.services.products_services import ProductServices

bp_products = Blueprint('products_view', __name__, url_prefix='/products')

@bp_products.route('/', methods=['GET'])
def get_products():
    return ProductServices.get_all_products(), HTTPStatus.OK


@bp_products.route('/<int:product_id>', methods=['GET'])
def get_products_id(product_id):
    return ProductServices.get_product_by_id(product_id)


@bp_products.route('/<int:id_prod>', methods=['DELETE'])
def delete_products_id(id_prod):
    
    session = current_app.db.session
    try:
        product_to_delete: ProductModel = ProductModel.query.get(id_prod)
        deleted = current_app.db.session.delete(product_to_delete)
    except:
        return {'result': 'Not Found'},HTTPStatus.NOT_FOUND
    session.commit()
    return {'data':'deleted'}, HTTPStatus.OK


@bp_products.route('/<int:id_prod>', methods=['PATCH'])
def path_products_id(id_prod):

    session = current_app.db.session
    found_user: ProductModel = ProductModel.query.get(id_prod)
    data = request.get_json()

    try:
        for key, value in data.items():
            setattr(found_user, key, value)
        session.add(found_user)
        session.commit()

        return {"user": 'found_user.name', "email": 'found_user.email'},HTTPStatus.OK
    except Exception as nome:
        return "test",HTTPStatus.BAD_REQUEST

