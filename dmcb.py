# Imports from Python Standard Library
from io import BytesIO
from threading import Lock, currentThread
from time import time
# Imports from flask, and dependencies
from flask import Flask, request, session,g, redirect, url_for, abort, \
     render_template, flash, send_file
from flask.ext.cache import Cache
# Imports from Pillow
from PIL.Image import Image
# Imports from our package     
from generator import generate_big

# Create our app    
app = Flask(__name__)

# Make a default config
app.config.update(dict(
    CACHE_TYPE= 'simple',
    TIMEOUT= 5))

# Create our cache, it's after the config, because it needs some values from it
cache = Cache(app)
    
# Load a config from the environment variable, if it exists
app.config.from_envvar('DMCB_CONFIG', silent=True)

@app.route('/<name>/<adress>/<int:port>/banner.png')
@cache.cached(timeout=app.config['TIMEOUT'])
def banner(name, adress, port):
    response = big_banner(adress, port, name)
    if not response:
        abort(500)
    return response

@app.route('/<name>/<adress>/banner.png')
@cache.cached(timeout=app.config['TIMEOUT'])
def banner2(name, adress):
    response = big_banner(adress, 0, name)
    if not response:
        abort(500)
    return response

def big_banner(adress, port, name):
    ''' Get the apropiate response for a banner with the credentials
    '''
    app.logger.debug("Regenerating banner")
    image = generate_big(adress, port, name)
    if type(image) != Image:
        abort(500)
        return
    byteio = BytesIO()
    image.save(byteio, "PNG")
    byteio.seek(0)
    return send_file(byteio, mimetype='image/png')

# If the script is run itself, start a debug server
if __name__ == '__main__':
    app.run(debug=True)
