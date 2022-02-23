from os.path import join, dirname, realpath
upload_folder = 'shop/static/img/product-img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
class Config(object):
    SECRET_KEY = 'qwertyuiop123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = upload_folder