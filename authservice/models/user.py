from passlib.utils import unicode
from .meta import Base, TimestampMixin
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode
    )
from sqlalchemy.orm import relationship
from pyramid.security import Allow
from passlib.hash import sha256_crypt
from .group import user_group_table
import logging
log = logging.getLogger(__name__)


# TODO: salt password...use bcrypt if possible
class User(TimestampMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True)
    password = Column(Unicode(80), nullable=False)
    groups = relationship('Group', secondary=user_group_table, backref='memberships')

    @property
    def __acl__(self):
        return [
            (Allow, self.login, 'view'),
        ]

    def __init__(self, login, password):
        self.login = login
        self._make_hash(password)

    def _make_hash(self, password):
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        hash = sha256_crypt.encrypt(password)
        self.password = hash

    def validate_password(self, password):
        """Check a password against an existing hash."""
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        hash = self.password
        log.debug(password)
        return sha256_crypt.verify(password, hash)

    def change_password(self, old_password, new_password):
        if not self.validate_password(old_password):
            return 'Password is invalid'

        self._make_hash(new_password)
        return 'Password successfully changed'

    @property
    def groups_str(self):
        return ', '.join((g.name for g in self.groups))

    # def set_groups(self, group_list):
    #     user = dbsession.query(User).filter(User.id == user_id).one()
    #     groups = [Group.get_group_by_id(g) for g in group_list]
    #     user.groups = groups

    @classmethod
    def get_user(cls, login, dbsession):
        try:
            user = dbsession.query(User).filter(User.login == login).one()
            return user
        except Exception as e:
            print('Error retrieving user %s: ', e)
            return None

    @classmethod
    def get_users(cls, dbsession):
        users = dbsession.query(User).all()
        return users

    @classmethod
    def get_user_by_id(cls, user_id, dbsession):
        user = dbsession.query(User).filter(User.id == user_id).one()
        return user

    @classmethod
    def get_user_by_login(cls, user_login, dbsession):
        user = dbsession.query(User).filter(User.login == user_login).one()
        return user
