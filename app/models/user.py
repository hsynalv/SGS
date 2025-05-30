from flask_login import UserMixin
from mongoengine import Document, StringField, EmailField, BooleanField


class User(UserMixin, Document):
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, max_length=50)
    password = StringField(required=True)  # Şifreyi daha güvenli tutmak için hash'lemek gerekebilir
    is_active = BooleanField(default=True)  # Kullanıcı aktif mi?
    is_admin = BooleanField(default=False)  # Admin mi?

    meta = {'collection': 'users'}


    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "is_admin": self.is_admin
        }
