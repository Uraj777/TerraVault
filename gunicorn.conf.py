import os
import multiprocessing

# Bind to PORT environment variable set by Render/Heroku, default to 5000
port = os.environ.get('PORT', '5000')
bind = f"0.0.0.0:{port}"

# Production Worker & Thread counts for high concurrency
# WEB_CONCURRENCY is automatically set by many hosting providers
workers = int(os.environ.get('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get('PYTHON_MAX_THREADS', '2'))

# Performance tuning
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = 5

# Logging settings for production observability
loglevel = 'info'
accesslog = '-'  # Redirect access log to stdout
errorlog = '-'   # Redirect error log to stderr
capture_output = True
enable_inheritable_fds = True
