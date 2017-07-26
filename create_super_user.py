#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings

if __name__ == "__main__":
    django.setup()

    from django.contrib.auth.models import User

    username = os.environ.get('CATCHPY_ADMIN_USER', None)
    password = os.environ.get('CATCHPY_ADMIN_PASSWORD', None)
    if username and password:
        u = User(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
    else:
        raise NameError(
            "username or password missing - admin user not created")
    exit(0)

