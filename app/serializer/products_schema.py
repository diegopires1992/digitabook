from . import (
    marsh,
    ProductModel,
    AuthorModel,
    fields
)


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
