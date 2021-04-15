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
def get_product_by_id(product_id):
    return ProductServices.get_product_by_id(product_id)


@bp_products.route('/<int:product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    return ProductServices.delete_product(product_id)


@bp_products.route('/<int:product_id>', methods=['PATCH', 'PUT'])
def patch_product(product_id):
    data = request.get_json()
    return ProductServices.patch_product(product_id, data)


