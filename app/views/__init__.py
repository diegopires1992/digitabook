from flask import Flask


def init_app(app: Flask):
    from app.views.authors_view import bp_authors
    app.register_blueprint(bp_authors)

    from app.views.category_view import bp_category
    app.register_blueprint(bp_category)

    from app.views.products_view import bp_products
    app.register_blueprint(bp_products)

    from app.views.user_view import bp_user
    app.register_blueprint(bp_user)

    from app.views.order_view import bp_order
    app.register_blueprint(bp_order)
