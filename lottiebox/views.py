import os
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from lottiebox import lottiebox
from models import LottieBox as lbm
import helpers
from settings import LottieBoxSettings as lbs
from configparser import ConfigParser

## Load config
lottiebox_config = ConfigParser()
lottiebox_config.read(lbs.lb_config)
autoplay=lottiebox_config['USERCONFIG']['autoplay']
gallery=os.path.abspath(lottiebox_config['USERCONFIG']['lottiefiles'])

## Home
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
    sort=sort)

## Add
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

## File
@lottiebox.route('/lottiefiles/file/<path:filename>')
def lottiebox_file(filename):
    return send_from_directory(gallery, filename)

## Search
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

## Settings
@lottiebox.route("/lottiebox/settings", methods=['GET','POST'])
def lottiebox_settings():
  settings_form = lbm.SettingsForm()
  if settings_form.validate_on_submit():
    lottiebox_config = ConfigParser()
    lottiebox_config.read(lbs.lb_config)
    userconfig = lottiebox_config["USERCONFIG"]
    userconfig["autoplay"] = str(settings_form.autoplay_config.data)
    autoplay=userconfig["autoplay"]
    with open(lbs.lb_config, 'w') as conf:
      lottiebox_config.write(conf)
    # userconfig['gallery'] = settings_form.gallery_config
  return render_template("settings.html", settings_form=settings_form)

## View
@lottiebox.route('/lottiefiles/view/<path:filename>')
def lottiebox_view(filename):
  file_info = lbm.get_info(filename)
  tags = helpers.get_tags2(filename)
  related_files = lbm.get_related_files(tags, filename)
  return render_template("view.html",
    file_info=file_info,
    filename=filename,
    related_files=related_files)
