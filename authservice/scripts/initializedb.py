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
        dbsession.add(admin_group)
        dbsession.commit()
        admin_user = models.User('admin', 'admin')
        admin_user.groups = [admin_group]
        dbsession.add(admin_user)
        dbsession.commit()
        basic = models.Group('basic')
        dbsession.add(basic)
        dbsession.commit()
        basic_user = models.User('basic', 'basic')
        basic_user.groups = [basic]
        dbsession.add(basic_user)
        dbsession.commit()
        super_admin_group = models.Group('super_admin')
        dbsession.add(super_admin_group)
        dbsession.commit()
        super_admin_user = models.User('super_admin', 'super_admin')
        super_admin_user.groups = [super_admin_group]
        dbsession.add(super_admin_user)
        dbsession.commit()
