#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from dmcb import app

CGIHandler().run(app)
