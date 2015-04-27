from Server.Domain.Core import Jsonable


class UserDTO(Jsonable):
    def __init__(self, user):
        if user is not None:
            if user.id:
                self.id = user.id
            if user.display_name:
                self.displayName = user.display_name
            if user.pic_link:
                self.picture = user.pic_link
            if user.email:
                self.email = user.email
            if user.facebook:
                self.facebook = user.facebook
