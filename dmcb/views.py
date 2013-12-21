# Package: dmcb
from flask import abort, send_file;

from dmcb import app, cache, generator;

# The views:

@app.route('/<name>/<adress>/banner.png')
def name_adress(name, adress):
    return send_file(generator.banner(name, adress), mimetype="image/png", 
                     as_attachment=False)

@app.route('/<name>/<adress>/<int:port>/banner.png')
def name_adress_port(name, adress, port):
    return send_file(generator.banner(name, adress, port=port), 
                     mimetype="image/png", as_attachment=False)
    
