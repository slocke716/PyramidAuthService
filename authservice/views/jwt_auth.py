from authservice.models.user import User
import jwt
import logging


class JWTAuthView(object):
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def authenticate(self, login, password):
        user = User.get_user(login, self.request.dbsession)
        self.log.debug(login)
        self.log.debug('test')
        if user and user.validate_password(password):
            return user
        return None

    def login(self):
        try:
            login = self.request.POST.get('login', None)
            password = self.request.POST.get('password', None)
            self.log.debug('before auth')
            user = self.authenticate(login, password)
            self.log.debug('after auth')
            if user:
                token = self.request.create_jwt_token(user.id, roles=['role:%s' % g.name for g in user.groups])
                self.log.debug(token)
                decoded = jwt.decode(token, 'nottheseekrit', algorithms=['HS512'], verify=False)
                return dict(
                    success=True,
                    token=token,
                    exp=decoded.get('exp'),
                    iat=decoded.get('iat')
                )
            else:
                return dict(success=False, error='user was not authenticated')
        except Exception as e:
            self.log.debug(e.args[0])
            return dict(success=False, error='hit exception')


def includeme(config):
    config.add_route('login', '/login')
    config.add_view(JWTAuthView,
                    attr='login',
                    request_method='POST',
                    renderer='json',
                    route_name='login',
                    permission='__no_permission_required__')
