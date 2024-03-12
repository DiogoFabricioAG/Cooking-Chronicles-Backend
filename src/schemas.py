from ma import ma
from marshmallow import fields
from models import UserModel,Recipe
class UserSchema(ma.SQLAlchemyAutoSchema):
    image = fields.Method("get_image_url")

    def get_image_url(self, obj):
        if obj.image:
            return f"http://127.0.0.1:5000/api/user/{obj.id}/image"
        return None
    class Meta:
        model = UserModel
        fields = ('id','username','image','description','education','age','nationality','rank','speciality','count_recipes','linkface',"linktik","linkinsta")

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    image = fields.Method("get_image_url")
    def get_image_url(self, obj):
        if obj.image:
            return f"http://127.0.0.1:5000/api/recipes/{obj.id}/image"
        return None
    class Meta:
        model = Recipe
        include_fk = True
        fields = ("id", "name", "description", "user_impressions", "image", "user_model_id")

recipe_schema = RecipeSchema()
