from sqlalchemy.orm import backref

from . import db

class ProductModel(db.Model):
    
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=True)
    publisher = db.Column(db.String, nullable=False)
    isbn13 = db.Column(db.String, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=True)

    author_list = db.relationship(
        'AuthorModel', backref=db.backref(
            'products_list',
            lazy='joined',
        ), secondary='authors_products' 
    )

