import os
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from lottie import lottiebox
from models import LottieBox as lbm
import helpers
from settings import LottieBoxSettings as lbs
from configparser import ConfigParser

# Read lb_config.ini file
lottiebox_config = ConfigParser()
lottiebox_config.read(lbs.lb_config)
autoplay=lottiebox_config['USERCONFIG']['autoplay']
gallery=os.path.abspath(lottiebox_config['USERCONFIG']['lottiefiles'])

@lottiebox.route("/", methods=['GET'])
@lottiebox.route("/lottiebox")
def lottiebox_index():
  order = request.args.get("order")
  sort = request.args.get("sort")
  query_results = lbm.get_lottiefiles()
  return render_template(
    "index.html",
    query_results=query_results,
    order=order,
    sort=sort,
  )

@lottiebox.route("/lottiebox/add", methods=['GET','POST'])
def lottiebox_add():
  form = lbm.UploadFileForm()
  if form.validate_on_submit():
    file = form.file.data
    upload_filename = form.file.data.filename
    upload_url = os.path.join(gallery,upload_filename)
    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), gallery, secure_filename(file.filename)))
    message = upload_filename + ' has been uploaded.'
    return render_template("upload.html", form=form, message=message, upload_filename=upload_filename, upload_url=upload_url)

  return render_template("upload.html", form=form)

@lottiebox.route('/lottiefiles/download/<path:filename>')
def lottiebox_file(filename):
    return send_from_directory(gallery, filename)

@lottiebox.route("/lottiebox/search", methods=['GET'])
def lottiebox_search():
  order = request.args.get("order")
  sort = request.args.get("sort")
  query = request.args.get("q")
  query_results = lbm.search_query(query)
  
  return render_template(
    "index.html",
    query_results=query_results,
    order=order,
    sort=sort
  )

@lottiebox.route("/lottiebox/settings", methods=['GET','POST'])
def lottiebox_settings():
  settings_form = lbm.SettingsForm()
  if settings_form.validate_on_submit():
    lottiebox_config = ConfigParser()
    lottiebox_config.read(lbs.lb_config)
    userconfig = lottiebox_config["USERCONFIG"]
    userconfig["autoplay"] = str(settings_form.autoplay_config.data)
    with open(lbs.lb_config, 'w') as conf:
      lottiebox_config.write(conf)
    # userconfig['gallery'] = settings_form.gallery_config
  return render_template("settings.html", settings_form=settings_form)

@lottiebox.route('/lottiefiles/view/<path:filename>')
def lottiebox_view(filename):
  return render_template("view.html", filename=filename)