import os, time
import datetime as dt
import random

from configparser import ConfigParser
from flask import Flask, render_template
from flask_wtf import FlaskForm
from key_generator.key_generator import generate
from tkinter import filedialog
from tkinter import *
from wtforms import BooleanField, FileField, RadioField, StringField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from lottiebox import lottiebox
from settings import LottieBoxSettings as lbs

## Load config
lottiebox_config = ConfigParser()

## Init lb_config.ini with default settings if it does not exist
if not os.path.exists(lbs.lb_config):
  key = generate(max_atom_len = 64, min_atom_len = 64, num_of_atom = 1, separator = '')

  ## Request directory dialog screen
  root = Tk()
  root.withdraw()
  folder_selected = filedialog.askdirectory(title = "Select LottieFile directory.")

  ## Create config.ini
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
  ## Read lb_config.ini file
  lottiebox_config = ConfigParser()
  lottiebox_config.read(lbs.lb_config)

## Load user settings
autoplay=lottiebox_config['USERCONFIG']['autoplay']
gallery=os.path.abspath(lottiebox_config['USERCONFIG']['lottiefiles'])

## Create lottiesfiles directory if missing
if not os.path.exists(gallery):
  os.makedirs(gallery)

## Finish loading modules after loading config
import helpers

## Create LottieBox model
class LottieBox:
  lottiebox.config['SECRET_KEY'] = lottiebox_config['SYSCONFIG']['key']

  ## Forms
  class SettingsForm(FlaskForm):
    if autoplay == "True":
      autoplay_config = BooleanField(default="checked")
    else:
      autoplay_config = BooleanField()
    submit = SubmitField("Save Settings")

  class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Add File")

  ## Functions
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

  def get_info(filename):
    f = os.path.join(gallery,filename)
    
    taglist=''
    if f:
      modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(f)))
      # print(modified)
      basename = filename
      slug = filename; slug = slug.split('.'); slug = slug[0]
      caption = helpers.deslugify(filename)
      lottiepath = gallery + '/' + filename
      file_size = os.path.getsize(f)
      file_size = helpers.sizeof_fmt(file_size)
    return basename,caption,file_size,lottiepath,modified,slug

  def get_lottiefiles():
    lottiefiles=[]; n=0
    for gallery_file in sorted(os.listdir(gallery)):
      file_info = LottieBox.get_info(gallery_file)
      basename = file_info[0]
      caption = file_info[1]
      file_size = file_info[2]
      lottiepath = file_info[3]
      modified = file_info[4]
      slug = file_info[5]
      lottiefiles += [{
        'basename': basename,
        'caption': caption,
        'file_size': file_size,
        'lottiepath': lottiepath,
        'modified': modified,
        'slug': slug
      }]
    return lottiefiles

  def get_related_files(tags, filename):
    all_related_files=[]; related_files=[]; n=0
    get_tags=tags.split(",")
    for t in get_tags:
      for g in sorted(os.listdir(gallery)):
        if (g.__contains__(t)) and (not g.__contains__(filename)):
          all_related_files+=[g]
    all_related_files = set(all_related_files)
    if len(all_related_files) > 5:
      all_related_files = random.sample(all_related_files, 5)
    for a in all_related_files:
      file_info = LottieBox.get_info(a)
      basename = file_info[0]
      caption = file_info[1]
      lottiepath = file_info[3]
      related_files += [{
        'basename': basename,
        'caption': caption,
        'lottiepath': lottiepath
      }]
    return related_files

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