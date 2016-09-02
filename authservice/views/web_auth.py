from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from authservice.models import User


class WebAuthView(object):
    def __init__(self, request):
        self.request = request

    def authenticate(self, login, password):
        user = User.get_user(login, self.request.dbsession)
        if user and user.validate_password(password):
            return user
        return None

    def get_login(self):
        next = self.request.params.get('next') or self.request.route_url('home')
        login = ''
        return {
            'login': login,
            'next': next,
            'request': self.request
        }

    def login(self):
        login = self.request.POST.get('login', '')
        password = self.request.POST.get('password', '')
        next = self.request.route_url('home') if self.request.GET.get('next') is None else self.request.GET.get('next')

        user = self.authenticate(login, password)
        if user:
            headers = remember(self.request, login)
            return HTTPFound(location=next, headers=headers)

        return {
            'login': login,
            'next': next,
            'request': self.request
        }

    def logout(self):
        headers = forget(self.request)
        next_url = self.request.route_url('home')
        return HTTPFound(location=next_url, headers=headers)


def includeme(config):
    config.add_route('login', '/login')
    config.add_view(WebAuthView,
                    attr='login',
                    request_method='GET',
                    renderer='/templates/login.jinja2',
                    route_name='login',
                    permission='__no_permission_required__')
    config.add_view(WebAuthView,
                    attr='login',
                    request_method='POST',
                    renderer='/templates/login.jinja2',
                    route_name='login',
                    permission='__no_permission_required__')
    config.add_route('logout', '/logout')
    config.add_view(WebAuthView,
                    attr='logout',
                    request_method='GET',
                    renderer='/templates/login.jinja2',
                    route_name='logout',
                    permission='__no_permission_required__')
