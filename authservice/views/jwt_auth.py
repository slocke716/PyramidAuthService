from authservice.models.user import User
import jwt


class JWTAuthView(object):
    def __init__(self, request):
        self.request = request

    def authenticate(self, login, password):
        user = User.get_user(login, self.request.dbsession)
        if user and user.validate_password(password):
            return user
        return None

    def login(self):
        login = self.request.POST['login']
        password = self.request.POST['password']
        user = self.authenticate(login, password)  # You will need to implement this.
        if user:
            token = self.request.create_jwt_token(user.id, roles=['role:%s' % g.name for g in user.groups])
            decoded = jwt.decode(token, 'nottheseekrit', algorithms=['HS512'], verify=False)
            return dict(
                result='ok',
                token=token,
                exp=decoded.get('exp'),
                iat=decoded.get('iat')
            )
        else:
            return dict(result='error')


def includeme(config):
    config.add_route('login', '/login')
    config.add_view(JWTAuthView,
                    attr='login',
                    request_method='POST',
                    renderer='json',
                    route_name='login',
                    permission='__no_permission_required__')
