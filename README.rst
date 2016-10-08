AuthService README
==================

Getting Started
---------------

include secret in pyramid application as well as any jwt auth settings if using jwt and session based auth(web auth)

EXAMPLE ADDITION TO INI
=======================

secret = seekrit
jwt.private_key = seekrit
jwt.expiration = 43200

========================

next include the package in the __init__.py like so:

web auth
========
config.include('authservice.views.web_auth')
config.include('authservice.web_security')

jwt auth
========
config.include('authservice.views.jwt_auth')
config.include('authservice.jwt_security')


==========================================

You will also want to include an initialize_auth_db.py script in your scripts directory

initialize_auth_db.ini
======================

import os
import sys
from authservice.scripts import initializedb

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    inv = initializedb.InitializeDb(settings['sqlalchemy.url'])
    inv.initialize_db()

======================================================

Also add this as an entry point in setup.py

[console_scripts]
      initialize_auth_db = myapp.scripts.initialize_auth_db:main


Then after running python setup.py develop you can initialize the auth db like so:

initialize_auth_db development.ini