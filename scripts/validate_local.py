# Ejecuta validate_migration.py contra el Apache local (certificado autofirmado, sin proxy)
import ssl, sys, os, runpy
ssl._create_default_https_context = ssl._create_unverified_context
for k in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy'):
    os.environ.pop(k, None)
import urllib.request
urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ssl._create_unverified_context())))
sys.argv = ['validate_migration.py'] + sys.argv[1:]
runpy.run_path('scripts/validate_migration.py', run_name='__main__')
