from .base_test import BaseTestCase, dummy_request
from authservice.models.user import User
from authservice.models.group import Group


def create_jwt_token(id):
    return dict(token=id)


class FunctionalTests(BaseTestCase):

    def test_create_user(cls):
        group = Group('basic')
        cls.dbsession.add(group)
        cls.dbsession.commit()
        basic = User('basic', 'basic')
        basic.groups = [group]
        cls.dbsession.add(basic)
        cls.dbsession.commit()

    def test_login_user_should_pass(cls):
        group = Group('basic')
        cls.dbsession.add(group)
        cls.dbsession.commit()
        basic = User('basic', 'basic')
        basic.groups = [group]
        cls.dbsession.add(basic)
        cls.dbsession.commit()
        from authservice.views.jwt_auth import AuthView
        request = dummy_request(cls.dbsession)
        request.POST['login'] = 'basic'
        request.POST['password'] = 'basic'
        request.create_jwt_token = create_jwt_token
        av = AuthView(request)
        response = av.login()
        assert(response.get('result') == 'ok')

    def test_login_user_should_fail(cls):
        group = Group('basic')
        cls.dbsession.add(group)
        cls.dbsession.commit()
        basic = User('basic', 'basic')
        basic.groups = [group]
        cls.dbsession.add(basic)
        cls.dbsession.commit()
        from authservice.views.jwt_auth import AuthView
        request = dummy_request(cls.dbsession)
        request.POST['login'] = 'basic'
        request.POST['password'] = 'wrong'
        request.create_jwt_token = create_jwt_token
        av = AuthView(request)
        response = av.login()
        assert(response.get('result') == 'error')

