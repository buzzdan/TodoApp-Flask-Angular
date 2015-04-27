from Server.Domain.Core import Jsonable


class UserDTO(Jsonable):
    def __init__(self, user=None):
        self.id = ''
        self.displayName = ''
        self.picture = ''
        self.email = ''
        if user is not None:
            self.id = user.id
            self.displayName = user.display_name
            self.picture = user.pic_link
            self.email = user.email
