from uuid import uuid1
from werkzeug.security import generate_password_hash, check_password_hash


class User():
    def __init__(self, email=None, password=None, display_name=None,
                 facebook=None, github=None, google=None, linkedin=None,
                 twitter=None):
        self.id = uuid1()
        if email:
            self.email = email.lower()
        if password:
            self.set_password(password)
        if display_name:
            self.display_name = display_name
        if facebook:
            self.facebook = facebook
        if github:
            self.github = github
        if google:
            self.google = google
        if linkedin:
            self.linkedin = linkedin
        if twitter:
            self.twitter = twitter

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return dict(id=self.id, email=self.email, displayName=self.display_name,
                    facebook=self.facebook, google=self.google,
                    linkedin=self.linkedin, twitter=self.twitter)
