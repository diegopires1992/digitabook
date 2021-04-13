from flask import Blueprint, request, current_app
from http import HTTPStatus
from app.models.product_model import ProductModel

bp_products = Blueprint('products_view', __name__, url_prefix='/products')
