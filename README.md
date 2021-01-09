# dmcb

**A Dynamic Minecraft Banner**

![Example banner](https://raw.githubusercontent.com/tlaundal/dmcb/master/skogliv.png)

### Installation:
create a virtualenv, and apply it. Then run:

    pip install -r requirements.txt

Configure your webserver with either the `dmcb.wsgi` or `dmcb.cgi` file. Some info may be found here: http://flask.pocoo.org/docs/deploying/.

If you are only going to test this for yourself, you may just do: python dmcb.py

### Usage:
Banners are available with the following URL schema:

    /<server name>/<server adress>/banner.png

or

    /<server name>/<server adress>/<server port>/banner.png

"webserver url" is the url you configured for you webserver, or `127.0.0.1:5000` if you just used `python dmcb.py`. Colors 
may be used in the server name by using the codes from here: http://www.minecraftwiki.net/wiki/Formatting_codes. Bold text works too.

### Public instances
Please note, these instances are unofficial, and may use code different from this repo

 * MCLive: http://status.mclive.eu/
 
