# Package: dmcb
from flask import abort, send_file;

from dmcb import app, cache, generator;

# The views:

@app.route('/<name>/<adress>/banner.png')
@app.route('/1.7/<name>/<adress>/banner.png')
def name_adress(name, adress):
    return send_file(wrapper(name, adress), mimetype="image/png",
                     as_attachment=False)

@app.route('/<name>/<adress>/<int:port>/banner.png')
@app.route('/1.7/<name>/<adress>/<int:port>/banner.png')
def name_adress_port(name, adress, port):
    return send_file(wrapper(name, adress, port=port),
                     mimetype="image/png", as_attachment=False)

@cache.memoize(timeout=app.config['TIMEOUT'])
def wrapper(name, adress, port = 25565):
    return generator.banner(name, adress, port=port)