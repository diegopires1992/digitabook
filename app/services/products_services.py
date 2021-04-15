from flask import Flask, current_app
from . import AuthorModel
from . import AuthorsProducts 
from . import ProductModel


class ProductServices:

    @staticmethod
    def create_book(book: ProductModel, author: AuthorModel):
        
        session = current_app.db.session
        
        new_book = ProductModel(**book)
        new_book.author_list.append(author)
        
        session.add(new_book)
        session.commit()

    @staticmethod
    def get_all_products():
        
        session = current_app.db.session
        products = ProductModel.query.all()
        session.commit()

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
        }
