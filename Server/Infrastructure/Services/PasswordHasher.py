from Server.Domain.Interfaces import IPasswordHasher
from werkzeug.security import generate_password_hash, check_password_hash


class WerkzeugPasswordHasher(IPasswordHasher):
    def encode(self, password):
        return generate_password_hash(password)

    def verify(self, password, hashed_password):
        return check_password_hash(hashed_password, password)

