from waitress import serve
from handlers.rutes import *
from handlers.api import *

# starting server
serve(app, host="localhost", port=8080)
