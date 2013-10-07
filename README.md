#dmcb

**A Dynamic Minecraft Banner**

### Installation:
create a virtualenv, and apply it
run install.sh as sudo

Then configure your webserver with one of the dmcb files, some info may be found here: http://flask.pocoo.org/docs/deploying/
I do not provide support for setting up your web server.

If you are only going to test this for yourself, you may just do: python dmcb.py

### Usage:
The images reside on this URL:

> \<webserver url\>/\<server name\>/\<server adress\>/banner.png

or

> \<webserver url\>/\<server name\>/\<server adress\>/\<server port\>/banner.png

"webserver url" is the url you configured for you webserver or 127.0.0.1:5000 if you just used "python dmcb.py"
