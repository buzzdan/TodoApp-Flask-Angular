from abc import ABCMeta, abstractmethod


class IUserRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, _id):
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def get_by_facebook_id(self, facebook_id):
        pass

    @abstractmethod
    def get_by_google_id(self, google_id):
        pass

    @abstractmethod
    def delete(self, _id):
        pass

    @abstractmethod
    def update(self, _id, user):
        pass

    @abstractmethod
    def add(self, user):
        pass