from sqlalchemy.orm import backref

from . import db

class ProductModel(db.Model):
    
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=True)
    isbn13 = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False) 
    image = db.Column(db.String, nullable=True)

    author_list = db.relationship(
        'AuthorModel', backref=db.backref(
            'products_list',
            lazy='joined',
        ), secondary='authors_products' 
    )
