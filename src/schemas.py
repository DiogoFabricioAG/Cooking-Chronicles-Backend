from ma import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username','img')