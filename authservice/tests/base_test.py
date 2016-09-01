import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(cls):
        from authservice import models
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from authservice.models.meta import Base
        from sqlalchemy.orm import sessionmaker

        cls.engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(cls.engine)

        # create a configured "Session" class
        Session = sessionmaker(bind=cls.engine)

        # create a Session
        cls.dbsession = Session()

    def tearDown(cls):
        from authservice.models.meta import Base
        Base.metadata.drop_all(bind=cls.engine)
