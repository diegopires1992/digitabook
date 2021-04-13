from . import db

class AuthorsProducts(db.Model):

    __tablename__ = 'authors_products'

    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey(
        'authors.id', onupdate='CASCADE', ondelete='CASCADE'
    ))

    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', onupdate='CASCADE', ondelete='CASCADE'
    ))
