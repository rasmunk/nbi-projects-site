from nbi_base.models import ShelveObject


class Project(ShelveObject):

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def serialize(self):
        return self.__dict__
