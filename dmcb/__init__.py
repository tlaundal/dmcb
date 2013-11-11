# __init__ file in dmcb package
from flask import Flask
from flask.ext.cache import Cache

global app, cache

# Init the flask app
app = Flask(__name__)
# Create a simple config
app.config.update(dict(
    CACHE_TYPE= 'simple',
    TIMEOUT= 5))
# Load config from file supplied in environment variable
app.config.from_envvar('DMCB_CONFIG', silent=True)
# Init the cache
cache = Cache(app)

# Import the views, Flask will automaticaly set them up
import dmcb.views
