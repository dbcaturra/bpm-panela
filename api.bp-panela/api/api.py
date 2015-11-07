"""api bpm-panela"""

import datetime

from flask import Blueprint, render_template, request, session, redirect
from flask.ext.restful import Api, reqparse, Resource

from flask.ext.cors import CORS

from google.appengine.ext import ndb
from google.appengine.ext import db

from .models import Poll, Photo

#aux api method
def to_json(o):
	"""
	Custom serializer function
	"""
	if isinstance(o, list):
		return [to_json(l) for l in o]
	if isinstance(o, dict):
		x = {}
		for l in o:
			x[l] = to_json(o[l])
		return x
	if isinstance(o, datetime.date):
		return o.isoformat()
	if isinstance(o, ndb.GeoPt):
		return {'lat': o.lat, 'lon': o.lon}
	if isinstance(o, ndb.Key):
		return o.id()
	if isinstance(o, ndb.Model):
		dct = o.to_dict()
		dct['id'] = o.key.id()
		return to_json(dct)
	return o

class EntityView(Resource):

	def get(self, model, entity_id):
		self.model = eval(model.capitalize())
		modelretrive = self.model.get_by_id(entity_id)
		entity_key = modelretrive.put()
		modelretrive = entity_key.get()
		if modelretrive != None:
			return to_json(modelretrive)
		else:
			return 'not exist'

	def delete(self, model, entity_id):
		self.model = eval(model.capitalize())
		modelretrive = self.model.get_by_id(job_id)
		try:
			modelretrive.delete()
			return 'Ok', 200
		except:
			return 'Error', 502

	def put(self, model, entity_id):
		self.model = eval(model.capitalize())
		modelretrive = self.model.get_by_id(entity_id)
		try:
			for key in self.model.to_dict():
				setattr(modelretrive, key, request.form[key])
			modelretrive.put()
			return 'Ok', 201
		except:
			return 'Error', 502

class EntityService(Resource):

	def get(self, model):
		self.model = eval(model.capitalize())
		retrive = self.model().query().fetch()
		return to_json(retrive)

	def post(self, model):
		self.model = eval(model.capitalize())
		self.model = self.model()
		if request.method == 'POST':
			try:
				for key in self.model.to_dict():
					print key, "key del form"
					if key == "file":
						file_ = request.files[key]
						setattr(self.model, key, db.Blob(file_.read()))
					else:
						try:
							setattr(self.model, key, request.form[key])
						except Exception as e:
							print "error en %s, %s"%(key,request.form[key]), e
				self.model.put()
				return 'Ok', 201
			except Exception as e:
				print e
		else:
			return 'Validation error', 502

class ResourceModel():
	def __init__(self, service):
		self.urlservice = service
		self.service = service.replace("/", "") + "_api"
		self.bp = Blueprint(self.service, __name__)
		CORS(self.bp)
		self.api = Api(self.bp)
		self.entityservice = EntityService
		self.entityview = EntityView
		self.api.add_resource(self.entityservice, '/service/<model>')
		self.api.add_resource(self.entityview, '/get/<model>/<int:entity_id>')

resource = ResourceModel("/api")
