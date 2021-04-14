from flask import Blueprint, request, current_app
from http import HTTPStatus
from app.models.product_model import ProductModel
from app.models.authors_model import AuthorModel

bp_products = Blueprint('products_view', __name__, url_prefix='/products')

@bp_products.route('/', methods=['GET'])
def get_products():
    
    session = current_app.db.session
    products = ProductModel.query.all()

    return {
        "products": [{
            "title": product.title, 
            "author_list": [{
                "name": author.name
                } for author in product.author_list
            ]} for product in products
    ]}, HTTPStatus.OK