import os
import sys

path = '/var/www/baldessari.densitydesign.org/baldessari'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = "baldessari_sketch.settings"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
