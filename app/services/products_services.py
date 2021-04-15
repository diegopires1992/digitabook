from flask import Flask, current_app
from http import HTTPStatus
from . import AuthorModel
from . import AuthorsProducts 
from . import ProductModel


class ProductServices:
    def __init__(self, session):
        self.session = session


    def create_book(self, book: ProductModel, author: AuthorModel):
        new_book = ProductModel(**book)
        new_book.author_list.append(author)
        
        self.session.add(new_book)
        self.session.commit()

        return True


    def get_all_products(self, request):
        products = ProductModel.query.all()

        return {
            'products': [{
                'id':product.id,
                'title': product.title,
                'subtitle': product.subtitle,
                'isbn13': product.isbn13,
                'price': product.price,
                'image_url': product.image, 
                'authors': [{
                    'name': author.name,
                    'birthplace': author.birthplace,
                    'book_list_url': f'http://deploy.url/products/?author_id={author.id}'
                    } for author in product.author_list
                ]} for product in products
            ]
        }, HTTPStatus.OK


    def get_product_by_id(self, product_id):
        found_product: ProductModel = ProductModel.query.get(product_id)

        if not found_product:
            response = {
                'Message': 'Product not found'
            }, HTTPStatus.UNPROCESSABLE_ENTITY

        else:
            response = {
            'id': found_product.id,
            'title': found_product.title,
            'subtitle': found_product.subtitle,
            'isbn13': found_product.isbn13,
            'price': found_product.price,
            'image_url': found_product.image
        }, HTTPStatus.OK

        return response


    def delete_product(self, product_id):
        product_to_delete: ProductModel = ProductModel.query.get(product_id)

        if not product_to_delete:
            response = {
                'Message': 'Product not Found'
            }, HTTPStatus.NOT_FOUND

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

            response = {
                'title': found_product.title, 
                'subtitle': found_product.subtitle,
                'isbn13': found_product.isbn13,
                'price': found_product.price,
                'image_url': found_product.image
            }, HTTPStatus.OK

            self.session.add(found_product)
            self.session.commit()


        except Exception as exception:
            response = {
                'Error': exception.args
            }, HTTPStatus.BAD_REQUEST

        return response
