from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .models.user import User
from .models.RootFactory import RootFactory
from .security import get_user
import logging
log = logging.getLogger(__name__)


def auth_callback(login, request):
    log.debug('auth_callback called with USER: {0}'.format(login))
    user = User.get_user(login, request.dbsession)
    if user and user.groups:
        group_list = ['role:%s' % g.name for g in user.groups]
        log.debug('auth_callback found GROUPS: {0} for USER: {1}'.format(group_list, login))
        return group_list
    elif user:
        log.debug('auth_callback found USER: {0}'.format(user))
        return [user.id]
    else:
        log.debug('auth_callback found no authentication credentials')
        return []


def includeme(config):
    settings = config.get_settings()
    authn_policy = AuthTktAuthenticationPolicy(
        settings['secret'],
        callback=auth_callback
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_root_factory(RootFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_request_method(get_user, 'user', reify=True)
