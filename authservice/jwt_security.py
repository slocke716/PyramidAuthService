from pyramid.authorization import ACLAuthorizationPolicy
from .models.RootFactory import RootFactory
from .security import get_user
import logging
log = logging.getLogger(__name__)


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
