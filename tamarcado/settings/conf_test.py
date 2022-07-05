from tamarcado.settings.dev import *

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'pytest'