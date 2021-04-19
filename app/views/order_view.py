from flask import Blueprint, request, current_app
from app.models.order_model import OrderModel
from app.models.user_model import UserModel
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_order = Blueprint("bp_order", __name__, url_prefix="/order")


@bp_order.route("/", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()

    found_user = UserModel.query.get(user_id)

    if not found_user:
        return {"msg": "user not found"}, HTTPStatus.NOT_FOUND

    session = current_app.db.session

    body = request.get_json()
    order_date = body.get("order_date")
    payment_status = body.get("payment_status")
    credit_card = body.get("credit_card")
    cvv = body.get("cvv")
    adress = body.get("adress")
    total_value = body.get("total_value")

    new_order = OrderModel(order_date=order_date, payment_status=payment_status,
                           credit_card=credit_card, cvv=cvv, adress=adress, total_value=total_value)

    found_user.orders_list.append(new_order)

    session.add(found_user)
    session.commit()

    return {
        "order":
            {
                "id": new_order.id,
                "date": new_order.order_date,
                "status": new_order.payment_status,
                "total": new_order.total_value
            }
    }, HTTPStatus.CREATED


@bp_order.route("/<int:order_id>", methods=["PUT"])
@jwt_required()
def edit_order():

    user_id = get_jwt_identity()

    found_user = UserModel.query.get(user_id)

    if not found_user:
        return {"msg": "user not found"}, HTTPStatus.NOT_FOUND


@bp_order.route("/", methods=["GET"])
@jwt_required()
def all_orders():

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
                "total": order.total_value
            } for order in found_user.orders_list
        ]
    }, HTTPStatus.OK


@bp_order.route("/<int:order_id>", methods=["DELETE"])
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
