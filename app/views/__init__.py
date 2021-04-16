from flask import Flask, Blueprint, request, current_app
from app.models.product_model import ProductModel
from app.models.authors_model import AuthorModel
from sqlalchemy import update
from app.services.products_services import ProductServices


def init_app(app: Flask):
    from app.views.authors_view import bp_authors
    app.register_blueprint(bp_authors)

    from app.views.category_view import bp_category
    app.register_blueprint(bp_category)

    from app.views.products_view import bp_products
    app.register_blueprint(bp_products)

    from app.views.user_view import bp_user
    app.register_blueprint(bp_user)
