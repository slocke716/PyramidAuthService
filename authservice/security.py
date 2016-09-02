from .models.user import User
from pyramid.security import unauthenticated_userid
import logging
log = logging.getLogger(__name__)


def get_user(request):
    login = unauthenticated_userid(request)
    if login is not None:
        return User.get_user_by_login(login, request.dbsession)

