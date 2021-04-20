from . import(
    marsh,
    UserModel,
    fields
)

class UsersSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        fields = (
           'name',
           'email' 
        )
        ordered = True
        laod_instance = True
    
    name = marsh.auto_field()
    email = marsh.auto_field()

    