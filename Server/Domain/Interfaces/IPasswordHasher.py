from abc import ABCMeta, abstractmethod


class IPasswordHasher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def encode(self, password):
        pass

    @abstractmethod
    def verify(self, password, hashed_password):
        pass