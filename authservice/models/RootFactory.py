from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS
    )


class RootFactory(object):
    __acl__ = [
        (Allow, 'role:super_admin', ALL_PERMISSIONS),
        (Allow, 'role:admin', 'admin'),
    ]

    def __init__(self, request):
        self.request = request
