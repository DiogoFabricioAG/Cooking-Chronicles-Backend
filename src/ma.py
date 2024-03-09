from flask_marshmallow import Marshmallow

ma = Marshmallow()
def ma_init(app):
    ma.init_app(app)
