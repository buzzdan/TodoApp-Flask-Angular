from Server.Domain.Core import Jsonable


class UserDTO(Jsonable):
    def __init__(self, user):
        if user is not None:

            if getattr(user, 'id', None):
                self.id = user.id

            if getattr(user, 'email', None):
                self.email = user.email

            if getattr(user, 'display_name', None):
                self.displayName = user.display_name

            if getattr(user, 'hashed_password', None):  # dont expose password to api object
                pass

            if getattr(user, 'facebook', None):
                self.facebook = user.facebook

            if getattr(user, 'google', None):
                self.google = user.google

            if getattr(user, 'twitter', None):
                self.twitter = user.twitter

            if getattr(user, 'github', None):
                self.github = user.github

            if getattr(user, 'pic_link', None):
                self.picture = user.pic_link

            if getattr(user, 'linkedin', None):
                self.linkedin = user.linkedin
