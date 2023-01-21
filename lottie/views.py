import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from lottie import app
from models import LottieBox as lbm

import helpers

@app.route("/")
def index():
  return render_template("index.html", body=lbm.create_file_list())

@app.route("/upload", methods=['GET','POST'])
def upload():
  form = lbm.UploadFileForm()
  if form.validate_on_submit():
    file = form.file.data
    upload_filename = form.file.data.filename
    upload_url = os.path.join(app.config['GALLERY'],upload_filename)
    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['GALLERY'], secure_filename(file.filename)))
    message = upload_filename + ' has been uploaded.'
    return render_template("upload.html", form=form, message=message, upload_filename=upload_filename, upload_url=upload_url)

  return render_template("upload.html", form=form)