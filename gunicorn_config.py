import os
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')
forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
project_root = os.path.dirname(os.path.abspath(__file__))  
accesslog = os.path.join(project_root, 'access.log')  
errorlog = os.path.join(project_root, 'error.log')  
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'debug')  
