#!/bin/bash
pip install Pillow
pip install Flask
pip install dnspython3
git clone https://github.com/thadeusb/flask-cache.git
cd flask-cache
python setup.py install
cd ..
rm -r flask-cache
