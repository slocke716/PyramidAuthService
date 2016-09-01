from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS
    )


class RootFactory(object):
    __acl__ = [
        (Allow, 'g:super_admin', ALL_PERMISSIONS),
        (Allow, 'g:admin', 'admin'),
    ]

    def __init__(self, request):
        self.request = request
