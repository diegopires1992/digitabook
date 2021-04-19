from . import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    credit_card = db.Column(db.String(16), nullable=False, unique=True)
    cvv = db.Column(db.String(3), nullable=False)
    address = db.Column(db.String, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    client = db.relationship('UserModel', backref=db.backref(
        "orders_list", lazy='joined'), lazy='joined')
    list_products = db.relationship('ProductModel', backref=db.backref(
        "orders", lazy="joined"), secondary='order_products')
