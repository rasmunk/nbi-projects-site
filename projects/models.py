from nbi_base.models import ShelveObject


class Project(ShelveObject):

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def serialize(self):
        return self.__dict__


class User(ShelveObject):

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def serialize(self):
        return self.__dict__

    @staticmethod
    def valid_user(email, password):
        users = User.get_all()
        for user in users:
            if user.email == email and user.password == password:
                return True
        return False

    def is_authenticated(self):
        return self.__dict__['is_authenticated']

    def is_active(self):
        return self.__dict__['is_active']

    def is_anonymous(self):
        return self.__dict__['is_anonymous']

    def get_id(self):
        return self.__dict__['_id']