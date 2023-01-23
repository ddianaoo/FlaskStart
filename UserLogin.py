from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):

    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id=user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['username'] if self.__user else "This user haven`t name"

    def getEmail(self):
        return self.__user['email'] if self.__user else "This user haven`t email"

    def getPhoto(self, app):
        img = None
        if not self.__user['photo']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='img/default.jpg'), 'rb') as f:
                    img = f.read()
            except FileNotFoundError as e:
                print('file for default not found'+str(e))
        else:
            img = self.__user['photo']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        return ext.lower() in ('jpg', 'png')