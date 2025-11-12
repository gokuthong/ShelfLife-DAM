<<<<<<< HEAD
"""
WSGI config for ShelfLifeDAM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

=======
import os
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShelfLifeDAM.settings')

<<<<<<< HEAD
application = get_wsgi_application()
=======
application = get_wsgi_application()
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
