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
