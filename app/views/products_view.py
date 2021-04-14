from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from app.models.product_model import ProductModel
from app.models.authors_model import AuthorModel
from sqlalchemy import update

bp_products = Blueprint('products_view', __name__, url_prefix='/products')

@bp_products.route('/', methods=['GET'])
def get_products():
    
    session = current_app.db.session
    products = ProductModel.query.all()
    session.commit()
    return {
        "products": [{
            "title": product.title, 
            "author_list": [{
                "name": author.name
                } for author in product.author_list
            ]} for product in products
    ]}, HTTPStatus.OK


@bp_products.route('/<int:id_prod>', methods=['GET'])
def get_products_id(id_prod):
    
    session = current_app.db.session
    products = ProductModel.query.get(id_prod)
    session.commit()
    return {'id':products.id,
            'title':products.title,
            'subtitle':products.subtitle,
            'publisher':products.publisher,
            'isbn13':products.isbn13,
            'pages':products.pages,
            'description':products.description,
            'price':products.price,
            'image_url':products.image_url}, HTTPStatus.OK

@bp_products.route('/<int:id_prod>', methods=['DELETE'])
def delete_products_id(id_prod):
    
    session = current_app.db.session
    try:
        product_to_delete = ProductModel.query.get(id_prod)
        deleted = current_app.db.session.delete(product_to_delete)
    except:
        return {'result': 'Not Found'},HTTPStatus.NOT_FOUND
    session.commit()
    return {'data':'deleted'}, HTTPStatus.OK


@bp_products.route('/<int:id_prod>', methods=['PATCH'])
def path_products_id(id_prod):

    body = request.get_json()

    session = current_app.db.session



    product_to_update = ProductModel.query.get(id_prod)
    product_to_update.query.update(body)

    session.add(product_to_update)

    session.commit()

    return {'data':'deleted'}, HTTPStatus.OK