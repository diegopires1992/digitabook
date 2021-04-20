from flask import Blueprint, request, current_app
from app.models.order_model import OrderModel
from app.models.user_model import UserModel
from app.models.product_model import ProductModel
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_order = Blueprint("bp_order", __name__, url_prefix="/order")


@bp_order.route("/add", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()

    found_user: UserModel = UserModel.query.get(user_id)

    if not found_user:
        return {"msg": "user not found"}, HTTPStatus.NOT_FOUND

    session = current_app.db.session

    body = request.get_json()
    order_date = body.get("order_date")
    credit_card = body.get("credit_card")
    cvv = body.get("cvv")
    address = body.get("address")
    total_value = body.get("total_value")
    items = body.get("items")

    new_order: OrderModel = OrderModel(
        order_date=order_date,
        credit_card=credit_card,
        cvv=cvv,
        address=address,
        total_value=total_value
    )

    new_order.set_payment_status()

    products = session.query(ProductModel).filter(
        ProductModel.id.in_(items)).all()

    new_order.list_products = products
    found_user.orders_list.append(new_order)

    session.add(found_user)
    session.commit()

    return {
        "order":
            {
                "id": new_order.id,
                "date": new_order.order_date,
                "status": new_order.payment_status,
                "total": new_order.total_value,
                "products": [
                    {
                        "id": product.id,
                        "title": product.title,
                        "subtitle": product.subtitle,
                        "price": product.price
                    } for product in new_order.list_products
                ]
            }
    }, HTTPStatus.CREATED


@bp_order.route("/edit/<int:order_id>", methods=["PUT"])
@jwt_required()
def edit_order(order_id):

    try:
        session = current_app.db.session

        body = request.get_json()

        user_id = get_jwt_identity()

        found_order: OrderModel = OrderModel.query.get(order_id)

        if found_order.user_id != user_id:
            return {"msg": "Not Authorized"}, HTTPStatus.UNAUTHORIZED

        found_order.order_date = body['order_date']
        found_order.credit_card = body['credit_card']
        found_order.cvv = body['cvv']
        found_order.address = body['address']
        found_order.total_value = body['total_value']

        session.add(found_order)
        session.commit()

        return {
            'order': {
                "id": found_order.id,
                "date": found_order.order_date,
                "status": found_order.payment_status,
                "total": found_order.total_value
            }
        }, HTTPStatus.OK

    except:
        return {"msg": "Requisition error"}, HTTPStatus.BAD_REQUEST


@bp_order.route("/all", methods=["GET"])
@jwt_required()
def all_orders():

    try:

        user_id = get_jwt_identity()

        found_user = UserModel.query.get(user_id)

        if not found_user:
            return {"msg": "user not found"}, HTTPStatus.NOT_FOUND

        return {
            "orders": [
                {
                    "id": order.id,
                    "date": order.order_date,
                    "status": order.payment_status,
                    "total": order.total_value,
                    "products": [
                        {
                            "id": product.id,
                            "title": product.title,
                            "subtitle": product.subtitle,
                            "price": product.price
                        } for product in order.list_products
                    ]

                } for order in found_user.orders_list
            ]
        }, HTTPStatus.OK

    except:
        return {"orders": []}, HTTPStatus.OK


@bp_order.route("/delete/<int:order_id>", methods=["DELETE"])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()

    try:
        session = current_app.db.session

        found_order: OrderModel = OrderModel.query.get(order_id)

        if found_order.user_id != user_id:
            return {"msg": "Not Authorized"}, HTTPStatus.UNAUTHORIZED

        session.delete(found_order)
        session.commit()

        return {}, HTTPStatus.NO_CONTENT

    except Exception:
        return {"order not found"}, HTTPStatus.NOT_FOUND
