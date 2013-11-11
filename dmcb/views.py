# Package: dmcb
# abort(http code) and sendfile(file) function
from flask import abort, send_file;
# The Flask app and cache and the generator
from dmcb import app, cache, generator;

# The views:

@app.route('/<name>/<adress>/banner.png')
@app.cache.cached(timeout=app.config['TIMEOUT'])
def name_adress(name, adress):
    return send_file(generator.banner(name, adress), mimetype="image/png")

@app.route('/<name>/<adress>/<int:port>/banner.png')
@cache.cached(timeout=app.config['TIMEOUT'])
def name_adress_port(name, adress, port):
    return send_file(generator.banner(name, adress, port=port)

@app.route('/<version>/<name>/<adress>/banner.png')
@cache.cached(timeout=app.config['TIMEOUT'])
def version_name_adress(version, name, adress):
    if not (version == '1.7' or version == '1.6'):
        abort(404)
        return
    return send_file(generator.banner(name, adress, version=version), mimetype="image/png")

@app.route('/<version>/<name>/<adress>/<int:port>/banner.png')
@cache.cached(timeout=app.config['TIMEOUT'])
def version_name_adress_port(version, name, adress, port):
    if not (version == '1.7' or version == '1.6'):
        abort(404)
        return
    return send_file(generator.banner(name, adress, port=port, version=version), mimetype="image/png")
