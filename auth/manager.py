from database.models import User
import inject
from auth.validation import UserValidation


class DatabaseManager:

    def __init__(self):
        self.s = inject.instance("dbsession")

    def get_user_by_email(self, email):
        try:
            return self.s.query(User).filter_by(email=email).first()
        except Exception as e:
            print(e)

    def add_user(self, user_obj):
        UserValidation(user_obj).validate_and_raise()
        user = User(
            email=user_obj.get("email"),
            name=user_obj.get("name"),
            password=user_obj.get("password")
        )
        try:
            self.s.add(user)
            self.s.commit()
        except Exception as e:
            print(e)


