from sqlalchemy_mixins.utils import classproperty


class UserContext:
    _user = None

    @classmethod
    def set_user(cls, user):
        """
        :type user: user | UserDB
        """
        cls._user = user

    @classproperty
    def context_user_session(cls):
        """
        :rtype: user | UserDB
        """
        return cls._user
