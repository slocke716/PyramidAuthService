from authservice.models.user import User
import jwt
import logging
from pyramid.httpexceptions import HTTPUnauthorized, HTTPInternalServerError
logger = logging.getLogger(__name__)

class JWTAuthView(object):
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def authenticate(self, login, password):
        user = User.get_user(login, self.request.dbsession)
        if user and user.validate_password(password):
            return user
        return None

    def login(self):
        try:
            po = self.request.json_body
            login = po.get('login', None)
            password = po.get('password', None)
            user = self.authenticate(login, password)
            if user:
                token = self.request.create_jwt_token(user.id, roles=['role:%s' % g.name for g in user.groups])
                decoded = jwt.decode(token, 'nottheseekrit', algorithms=['HS512'], verify=False)
                return dict(
                    success=True,
                    token=token,
                    exp=decoded.get('exp'),
                    iat=decoded.get('iat')
                )
            else:
                return HTTPUnauthorized(json_body={'error': 'User was not authorized'})
        except Exception as e:
            logger.exception(e.args[0])
            raise HTTPInternalServerError(json_body={'error': 'An unknown error has occurred'})


def includeme(config):
    config.add_route('login', '/login')
    config.add_view(JWTAuthView,
                    attr='login',
                    request_method='POST',
                    renderer='json',
                    route_name='login',
                    permission='__no_permission_required__')
