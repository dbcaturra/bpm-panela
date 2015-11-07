from flask import session, redirect, g, request, url_for
from jinja2 import Markup

from flask_admin.contrib.appengine.view import NdbModelView
from flask_admin.base import AdminIndexView, expose
import flask_wtf

from google.appengine.ext import ndb

#from salusgp.adminauth import access

class AdminPoll(NdbModelView):
	# @access
	# def is_accessible(self):
	# 	pass
	#
	# def _handle_view(self, name, **kwargs):
	# 	if not self.is_accessible():
	# 		return redirect(url_for("frontendbp.login"))

	form_base_class = flask_wtf.Form
	can_delete = True  # disable model deletion
	page_size = 20
	column_list = ('created', 'qusername', 'qisvalid')
	column_formatters = dict(photos=lambda v, c, m, p: Markup(["<a href='/api/service/getphoto/%s' />%s</a>"%(photo, photo) for photo in m.file]))

class AdminPhoto(NdbModelView):
	# @access
	# def is_accessible(self):
	# 	pass
	#
	# def _handle_view(self, name, **kwargs):
	# 	if not self.is_accessible():
	# 		return redirect(url_for("frontendbp.login"))

	form_base_class = flask_wtf.Form
	page_size = 20
	can_delete = True  # disable model deletion
	column_list = ('id', 'created', 'filename', 'photo')
	column_formatters = dict(photo=lambda v, c, m, p: Markup("<img src='/api/service/getphoto/%s' />"%m.filename))

from .models import Photo
class PhotosView(AdminIndexView):
	@expose('/')
	def index(self):
		try:
			u = Photo.query().fetch()
			return self.render('listphotos.html', photos=u)
		except Exception as e:
			return e
