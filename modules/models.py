import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from lottie import app

import helpers

class LottieBox:
  app.config['SECRET_KEY'] = 'wecantstopherethisisbatcountry'
  app.config['GALLERY'] = 'static/gallery'

  class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

  def create_file_list():
    cw=4; lottiefiles =''; n=0;

    for gallery_file in sorted(os.listdir(app.config['GALLERY'])):
      f = os.path.join(app.config['GALLERY'],gallery_file)
      taglist=''
      if os.path.isfile(f):
        n = (n+1)
        basename = os.path.basename(f)
        caption = helpers.deslugify(basename)
        
        lottiepath = app.config['GALLERY'] + '/' + basename
        lottiefiles +='<div class="column is-3">\n'
        lottiefiles +='  <div class="card">\n'
        lottiefiles +='    <div class="card-image">\n'
        lottiefiles +='      <figure class="lottiefile image is-128x128">\n'
        lottiefiles +='        <lottie-player src="' + lottiepath + '" background="transparent"  speed="1" loop hover></lottie-player>'
        lottiefiles +='      </figure>\n'
        lottiefiles +='    </div>\n'
        lottiefiles +='    <div class="card-content"><a href="' + lottiepath + '">' + caption + '</a></div>\n'
        lottiefiles +='  </div>\n'
        lottiefiles +='</div>\n\n'
        if n % cw == 0:
          lottiefiles +='</div>\n\n<div class="columns">\n'
    
    return lottiefiles

