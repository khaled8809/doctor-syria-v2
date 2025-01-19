# Gunicorn configuration file

# Server socket
bind = "unix:/run/gunicorn.sock"
backlog = 2048

# Worker processes
workers = 3
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Process naming
proc_name = "doctor_syria"

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process management
daemon = False
pidfile = "/run/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Server mechanics
preload_app = True
reload = False
spew = False
check_config = False


# Server hooks
def on_starting(server):
    pass


def on_reload(server):
    pass


def when_ready(server):
    pass


def pre_fork(server, worker):
    pass


def post_fork(server, worker):
    pass


def pre_exec(server):
    pass


def pre_request(worker, req):
    worker.log.debug("%s %s" % (req.method, req.path))


def post_request(worker, req, environ, resp):
    pass


def child_exit(server, worker):
    pass


def worker_abort(worker):
    pass
