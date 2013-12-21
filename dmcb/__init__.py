# __init__ file in dmcb package
import os

from flask import Flask
from flask.ext.cache import Cache

global app, cache

# Init the flask app
app = Flask(__name__)
# Create a simple config
app.config.update(dict(
    CACHE_TYPE= 'simple',
    TIMEOUT= 0))
# Load config from file supplied in environment variable
app.config.from_envvar('DMCB_CONFIG', silent=True)
# Init the cache
cache = Cache(app)

# The root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
def get_path(path):
    return os.path.join(ROOT_DIR, path)


# Import the views, Flask will automaticaly set them up
import dmcb.views
