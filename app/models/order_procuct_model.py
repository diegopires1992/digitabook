from . import db

class OrderProducts(db.Model):

    __tablename__ = 'order_products'

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', onupdate='CASCADE', ondelete='CASCADE'
    ))

    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', onupdate='CASCADE', ondelete='CASCADE'
    ))
