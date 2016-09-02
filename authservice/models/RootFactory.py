from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS
    )


# TODO: get groups working with pyramid_jwt
class RootFactory(object):
    """currently for the sake of the api I will be using Authenticated for permission...
    this lacks fine-grain control and must be changed"""
    __acl__ = [
        (Allow, 'g:super_admin', ALL_PERMISSIONS),
        (Allow, 'g:admin', 'admin'),
        (Allow, Authenticated, ('admin',)),
    ]

    def __init__(self, request):
        self.request = request
