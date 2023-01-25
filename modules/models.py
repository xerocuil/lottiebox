import os, time
import datetime as dt

from configparser import ConfigParser
from flask import Flask, render_template
from flask_wtf import FlaskForm
from key_generator.key_generator import generate
from tkinter import filedialog
from tkinter import *
from wtforms import BooleanField, FileField, RadioField, StringField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from lottie import lottiebox
from settings import LottieBoxSettings as lbs

## Load config
lottiebox_config = ConfigParser()

## Init lb_config.ini with default settings if it does not exist
if not os.path.exists(lbs.lb_config):
  key = generate(max_atom_len = 64, min_atom_len = 64, num_of_atom = 1, separator = '')

  root = Tk()
  root.withdraw()
  folder_selected = filedialog.askdirectory(title = "Select LottieFile directory.")

  lottiebox_config["USERCONFIG"] = {
    "autoplay": "False",
    "lottiefiles": os.path.join(folder_selected)
  }

  lottiebox_config["SYSCONFIG"] = {
    "key": key.get_key(),
  }
  with open(lbs.lb_config, 'w') as conf:
    lottiebox_config.write(conf)
else:
  # Read lb_config.ini file
  lottiebox_config = ConfigParser()
  lottiebox_config.read(lbs.lb_config)

autoplay=lottiebox_config['USERCONFIG']['autoplay']
gallery=os.path.abspath(lottiebox_config['USERCONFIG']['lottiefiles'])

if not os.path.exists(gallery):
  os.makedirs(gallery)

import helpers

class LottieBox:
  lottiebox.config['SECRET_KEY'] = lottiebox_config['SYSCONFIG']['key']

  class SettingsForm(FlaskForm):
    if autoplay:
      autoplay_config = BooleanField(default="checked")
    else:
      autoplay_config = BooleanField()
    submit = SubmitField("Save Settings")

  class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Add File")

  def create_file_list():
    cw=4; lottiefiles =''; n=0;
    for gallery_file in sorted(os.listdir(gallery)):
      f = os.path.join(gallery,gallery_file)
      taglist=''
      if os.path.isfile(f):
        n = (n+1)
        basename = os.path.basename(f)
        caption = helpers.deslugify(basename)
        lottiepath = gallery + '/' + basename
        print(basename, caption, lottiepath)
    return lottiefiles

  def get_lottiefiles():
    lottiefiles=[]; n=0

    for gallery_file in sorted(os.listdir(gallery)):
      f = os.path.join(gallery,gallery_file)
      taglist=''
      if os.path.isfile(f):
        n = (n+1)
        modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(f)))
        basename = os.path.basename(f)
        slug = basename; slug = slug.split('.'); slug = slug[0]
        caption = helpers.deslugify(basename)
        lottiepath = gallery + '/' + basename
        lottiefiles += [{
          'basename': basename,
          'caption': caption,
          'lottiepath': lottiepath,
          'modified': modified,
          'slug': slug
        }]
    return lottiefiles

  def lottiefiles_arr(self):
    lottiefile_values = []
    lottiefiles = self.get_lottiefiles()
    for l in lottiefiles:
      lottiefile_values += [list(l.values())]
    return lottiefile_values

  def row_split(colwidth,index):
    if index % colwidth == 0:
      row_split = '</div><div class="columns">'
      return row_split

  def search_query(query):
    query_results = []
    for f in sorted(os.listdir(gallery)):
      fn = os.path.join(gallery,f)
      modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fn)))
      if f.__contains__(query):

        qr_file = f
        qr_caption = helpers.deslugify(f)
        query_results += [{
          'basename': qr_file,
          'caption': qr_caption,
          'modified': modified
          }]
    return query_results