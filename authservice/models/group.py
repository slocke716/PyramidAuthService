from .meta import Base, TimestampMixin
import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
    )
from sqlalchemy.orm import relationship
from pyramid.security import Allow
import logging
log = logging.getLogger(__name__)


user_group_table = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
)


class Group(TimestampMixin, Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    users = relationship('User', secondary=user_group_table, backref='members')

    @property
    def __acl__(self):
        # only allow members of this group to add new members
        access_list = [(Allow, 'g:{0}'.format(self.name), 'edit')]
        log.debug('GROUP access list: {0}'.format(access_list))
        return access_list

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_group(cls, name, dbsession):
        group = dbsession.query(Group).filter(Group.name == name).one()
        return group

    @classmethod
    def get_group_by_id(cls, id, dbsession):
        group = dbsession.query(Group).filter(Group.id == id).one()
        return group

    @classmethod
    def get_groups(cls, dbsession):
        groups = dbsession.query(Group).all()
        return groups
