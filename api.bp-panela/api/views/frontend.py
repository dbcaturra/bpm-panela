# -*- encoding:utf-8 -*-
from flask import Blueprint, redirect, render_template, request, make_response, session

from google.appengine.ext import db

from api.models import Photo

frontendbp = Blueprint('frontendbp',__name__)

@frontendbp.route('/')
def index():
    return "Hellow world"

@frontendbp.route('/api/service/getphoto/<id>')
def photo_service(id):
    try:
        u = Photo.query().filter(Photo.filename == id).fetch()[0]
        if u:
            response = make_response(u.file)
            response.headers['Content-Disposition'] = 'attachment; filename=%s'%u.filename
            response.headers['Content-Type'] = "image/jpg"
            return response

    except Exception as e:
        print e
        return "Blob not found"

@frontendbp.route('/api/service/listphotos')
def listPhotos():
    try:
        u = Photo.query().fetch()
        return render_template("listphotos.html", photos=u)
    except Exception as e:
        return e


@frontendbp.route('/pollpush', methods=['POST'])
def pollPush():
    if request.method == "POST":
        name_ = request.form['name']
        email_ = request.form['email']
        subject_ = request.form['subject']
        message_ = request.form['message']

	#eMail
        name_ = "Usuario"
        email_ = "eMail"
        subject_ = "Buenas practicas manofactura Panela - Corredor tecnológico"
        message_ = "Se ha publicado una encuesta! puder verla en http://bpm-panela.appspot.com"
        from google.appengine.api import mail
        try:
            message = mail.EmailMessage(sender="bpm-panela@appspot.gserviceaccount.com",
                                        subject=subject_)
            message.to = "presidencia.asiac@ingeniagro.org, dbcaturra@gmail.com"
            message.body = "Mensaje: " + message_ + " enviado: " + email_ + " Nombre: " + name_
            message.send()
            return "Ok", 202
        except Exception as e:
            print e
