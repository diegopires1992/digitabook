from . import (
    Flask, 
    current_app, 
    ProductAuthorSchema, 
    HTTPStatus, 
    AuthorModel, 
    AuthorsProducts, 
    ProductModel,
    AuthorSchema
)
from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus

class AuthorServices:
    def __init__(self, session):
        self.session = session

    def get_all_authors(self):
        authors = AuthorModel.query.all()

        author_list = AuthorSchema(many=True).dump(authors) 

        return {'authors': author_list}, HTTPStatus.OK   




    def post_create_author(self, request):

        body = request.get_json()
        name = body.get('name')
        birthplace = body.get('birthplace')

        new_author = AuthorModel(name=name, birthplace=birthplace)

        self.session.add(new_author)
        try:
            self.session.commit()

        except Exception as exception:
            return AuthorSchema().author_exists(), HTTPStatus.NO_CONTENT
        
        return AuthorSchema().dump(new_author), HTTPStatus.OK    

    def get_authors_by_id_service(self, authors_id):
        found_author = AuthorModel.query.get(authors_id)

        if found_author:
            response = AuthorSchema().dump(found_author), HTTPStatus.OK    
        else:
            response = AuthorSchema().author_not_found(), HTTPStatus.UNPROCESSABLE_ENTITY  

        return response


    def delete_author(self, product_id):
        session = current_app.db.session

        try:

            found_author = AuthorModel.query.get(product_id)

            session.delete(found_author)
            session.commit()

            return {}, HTTPStatus.NO_CONTENT

        except Exception:

            return AuthorSchema().author_not_deleted(), HTTPStatus.NOT_FOUND  
