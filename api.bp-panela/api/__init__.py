# -*- encoding:utf-8 -*-
from flask import Flask, Blueprint
from .views.frontend import frontendbp

app = Flask(__name__)
app.register_blueprint(frontendbp, url_prefix='')

#Admin
from flask_admin import Admin, base
from .models import Poll, Photo
from .admin import AdminPoll, AdminPhoto, PhotosView

admin = Admin(app, name='BPM Panela', template_mode='bootstrap3', index_view=PhotosView())
admin.add_view(AdminPoll(Poll))
#admin.add_view(AdminPhoto(Photo))

#Api
from .api import resource
app.register_blueprint(resource.bp, url_prefix=resource.urlservice)

#CORS
from flask.ext.cors import CORS
cors = CORS(app, resources={r"/api/service/*": {"origins": "*"}})
#cors = CORS(app, resources={r"/api/service/photo": {"origins": "*"}})
