#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from flask import Flask
import settings

from api import app
app.config.from_object(settings)
