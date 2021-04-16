from . import (
    Blueprint, 
    request, 
    current_app, 
    ProductServices
)

bp_products = Blueprint(
        'products_view', 
        __name__, 
        url_prefix='/products'
    )

@bp_products.route('/<int:author_id>', methods=['POST'])
def create_product(author_id):
    session = current_app.db.session
    product = request.get_json()

    return ProductServices(
        session
    ).create_book(product, author_id)


@bp_products.route('/', methods=['GET'])
def get_products():
    session = current_app.db.session
    
    return ProductServices(
        session
    ).get_all_products(request)


@bp_products.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    session = current_app.db.session

    return ProductServices(
        session
    ).get_product_by_id(product_id)


@bp_products.route('/<int:product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    session = current_app.db.session

    return ProductServices(
        session
    ).delete_product(product_id)


@bp_products.route('/<int:product_id>', methods=['PATCH', 'PUT'])
def patch_product(product_id):
    session = current_app.db.session
    data = request.get_json()

    return ProductServices(
        session
    ).patch_product(product_id, data)
