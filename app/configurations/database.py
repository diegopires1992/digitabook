from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.authors_model import AuthorModel
    from app.models.category_model import CategoryModel
    from app.models.authors_products_model import AuthorsProducts
    from app.models.product_model import ProductModel
    from app.models.user_model import UserModel
