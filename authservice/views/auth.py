class AuthView(object):
    def __init__(self, request):
        self.request = request

    def authenticate(self, login, password):
        return True

    def login(self):
        login = self.request.POST['login']
        password = self.request.POST['password']
        user_id = self.authenticate(login, password)  # You will need to implement this.
        if user_id:
            return {
                'result': 'ok',
                'token': self.request.create_jwt_token(user_id)
            }
        else:
            return {
                'result': 'error'
            }


# def includeme(config):
#     config.add_route('login', '/login')
#     config.add_view(AuthView,
#                     attr='login',
#                     request_method='POST',
#                     renderer='json',
#                     route_name='login')
