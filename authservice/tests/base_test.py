import unittest
import webtest
from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTestCase(unittest.TestCase):
    def setUp(cls):
        from authservice import models
        from authservice import main
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from authservice.models.meta import Base
        from sqlalchemy.orm import sessionmaker

        # instantiate app
        settings = {
            'sqlalchemy.url': 'sqlite:///:memory:',
            'secret': 'seekrit',
            'jwt.private_key': 'seekrit',
            'jwt.expiration': '1',
        }
        app = main({}, **settings)
        cls.testapp = webtest.TestApp(app)

        session_factory = app.registry['dbsession_factory']
        cls.engine = session_factory.kw['bind']

        Base.metadata.create_all(cls.engine)

        # create a configured "Session" class
        Session = sessionmaker(bind=cls.engine)

        # create a Session
        cls.dbsession = Session()

    def tearDown(cls):
        from authservice.models.meta import Base
        Base.metadata.drop_all(bind=cls.engine)
