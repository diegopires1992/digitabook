from . import (
    marsh,
    ProductModel,
    AuthorModel,
    fields
)


class AuthorSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthorModel
        fields = (
            'id',
            'name',
            'birthplace'
        )
        ordered = True
        load_instance = True

    id = marsh.auto_field()
    name = marsh.auto_field()
    birthplace = marsh.auto_field()


    def author_not_found(self):
        return { 'Message': 'Author not found' }


    def author_not_deleted(self):
        return { 'Message': 'deleted not author' }


    def author_exists(self):
        return {"message":"Author already exists"}



class ProductAuthorSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        fields = (
            'id', 
            'title',
            'subtitle', 
            'price',
            'isbn13',
            'image',
            'author_list'
        )
        ordered = True
        load_instance = True
    
    id = marsh.auto_field()
    title = marsh.auto_field()
    subtitle = marsh.auto_field()
    price = marsh.auto_field()
    isbn13 = marsh.auto_field()
    image = marsh.auto_field()

    author_list = marsh.Nested(AuthorSchema(many=True))

    def product_not_found(self):
        return { 'Message': 'Product not found' }


    def author_not_found(self):
        return { 'Message': 'Author not found' }
