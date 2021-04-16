from . import (
    Flask, 
    current_app, 
    ProductAuthorSchema, 
    HTTPStatus, 
    AuthorModel, 
    AuthorsProducts, 
    ProductModel
)


class ProductServices:
    def __init__(self, session):
        self.session = session


    def create_book(self, book, author_id):
        
        author: AuthorModel = AuthorModel.query.get(author_id)

        required_values = (
            'title',
            'subtitle', 
            'price', 
            'isbn13', 
            'image'
        )

        if not all(received_values in required_values for received_values in book.keys()):
            raise Exception("Invalid keys")
        
        if author:
            new_book = ProductModel(**book)
            new_book.author_list.append(author)

            self.session.add(new_book)
            self.session.commit()

            response = ProductAuthorSchema().dump(new_book), HTTPStatus.CREATED
        
        else:
            response = ProductAuthorSchema().author_not_found(), HTTPStatus.UNPROCESSABLE_ENTITY
        
        return response

    def get_all_products(self, request):
        products = ProductModel.query.all()
        products_list = ProductAuthorSchema(many=True).dump(products)

        return {'products': products_list}, HTTPStatus.OK


    def get_product_by_id(self, product_id):
        found_product: ProductModel = ProductModel.query.get(product_id)

        if not found_product:
            response = ProductAuthorSchema().product_not_found(), HTTPStatus.UNPROCESSABLE_ENTITY

        else:
            response = ProductAuthorSchema().dump(found_product), HTTPStatus.OK

        return response


    def delete_product(self, product_id):
        product_to_delete: ProductModel = ProductModel.query.get(product_id)

        if not product_to_delete:
            response = ProductAuthorSchema().product_not_found(), HTTPStatus.UNPROCESSABLE_ENTITY

        else:
            deleted = self.session.delete(product_to_delete)
            self.session.commit()

            response = {}, HTTPStatus.NO_CONTENT

        return response


    def patch_product(self, product_id, data):
        found_product: ProductModel = ProductModel.query.get(product_id)
        acepted_values = ('title', 'subtitle', 'price', 'image',)

        try:
            if any(received_values not in acepted_values for received_values in data.keys()):
                raise Exception("Invalid keys")

            for key, value in data.items():
                setattr(found_product, key, value)

            response = ProductAuthorSchema().dump(found_product), HTTPStatus.OK

            self.session.add(found_product)
            self.session.commit()

        except Exception as exception:
            response = {
                'Error': exception.args
            }, HTTPStatus.BAD_REQUEST

        return response
