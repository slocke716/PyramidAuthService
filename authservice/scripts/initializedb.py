from sqlalchemy import create_engine

from authservice import models
from authservice.models.meta import Base
from sqlalchemy.orm import sessionmaker


class InitializeDb(object):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def initialize_db(self):
        engine = create_engine(self.connection_string)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # create a configured "Session" class
        Session = sessionmaker(bind=engine)

        # create a Session
        dbsession = Session()

        admin_group = models.Group('admin')
        admin_user = models.User('admin', 'admin')
        basic = models.Group('basic')
        basic_user = models.User('basic', 'basic')
        super_admin_group = models.Group('super_admin')
        super_admin_user = models.User('super_admin', 'super_admin')
        admin_group.users = [admin_user]
        super_admin_group.users = [super_admin_user]
        dbsession.add_all([admin_group, admin_user, super_admin_group, super_admin_user, basic, basic_user])
        dbsession.commit()
