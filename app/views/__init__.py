from flask import Flask


def init_app(app: Flask):
    from app.views.authors_view import bp_authors
    app.register_blueprint(bp_authors)

    from app.views.category_view import bp_category
    app.register_blueprint(bp_category)
