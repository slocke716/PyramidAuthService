from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .models.user import User
from .models.RootFactory import RootFactory
from pyramid.security import unauthenticated_userid
import logging
log = logging.getLogger(__name__)


def get_user(request):
    login = unauthenticated_userid(request)
    if login is not None:
        return User.get_user_by_login(login, request.dbsession)


def auth_callback(login, request):
    log.debug('auth_callback called with USER: {0}'.format(login))
    user = User.get_user(login, request.dbsession)
    if user and user.groups:
        group_list = ['g:%s' % g.name for g in user.groups]
        log.debug('auth_callback found GROUPS: {0} for USER: {1}'.format(group_list, login))
        return group_list
    elif user:
        log.debug('auth_callback found USER: {0}'.format(user))
        return [user.id]
    else:
        log.debug('auth_callback found no authentication credentials')
        return []


def add_role_principals(userid, request):
    return [role for role in request.jwt_claims.get('roles', [])]


def includeme(config):
    settings = config.get_settings()
    # Pyramid requires an authorization policy to be active.
    config.set_authorization_policy(ACLAuthorizationPolicy())
    # Enable JWT authentication.
    config.include('pyramid_jwt')
    secret = settings['secret']
    config.set_jwt_authentication_policy(secret, http_header='X-Token', callback=add_role_principals)
    config.set_root_factory(RootFactory)
    config.add_request_method(get_user, 'user', reify=True)
