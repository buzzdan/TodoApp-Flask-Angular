from uuid import uuid1


class User():
    def __init__(self, email=None, hashed_password=None, display_name=None,
                 facebook=None, github=None, google=None, linkedin=None,
                 twitter=None, pic_link=None):
        self.id = str(uuid1())
        if email:
            self.email = email.lower()
        if hashed_password:
            self.hashed_password = hashed_password
        if display_name:
            self.display_name = display_name
        self.facebook = facebook
        self.github = github
        self.google = google
        self.linkedin = linkedin
        self.twitter = twitter
        self.pic_link = pic_link

    def copy_user(self):
        u = User(email=self.email,
                    hashed_password=self.hashed_password,
                    display_name=self.display_name,
                    facebook=self.facebook,
                    github=self.github,
                    google=self.google,
                    linkedin=self.linkedin,
                    twitter=self.twitter,
                    pic_link=self.pic_link)
        u.id = self.id
        return u
