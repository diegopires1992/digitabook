from . import (
    marsh,
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
        return {'Message': 'Author not found'}

    def author_not_deleted(self):
        return {'Message': 'deleted not author'}

    def author_exists(self):
        return {"message": "Author already exists"}
