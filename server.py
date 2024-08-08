from waitress import serve
from handlers.rutes import *

# starting server
serve(app, host="localhost", port=8080)
