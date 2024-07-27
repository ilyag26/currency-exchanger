from waitress import serve
from rutes import *

serve(app, host="localhost", port=8080)