import os
import settings
from markupsafe import escape
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wecantstopherethisisbatcountry'
app.config['GALLERY'] = 'static/gallery'

app_title = settings.app_title
gallery = app.config['GALLERY']
appdir = (os.path.dirname(__file__))

tag_delim01 = '['
tag_delim02 = ']'

@app.context_processor
def utility_processor():
  def get_app_title():
    t = settings.app_title
    return t

  def get_version():
    return settings.version

  return dict(
    get_app_title=get_app_title,
    get_version=get_version
    )

print(app.config['GALLERY'])

class UploadFileForm(FlaskForm):
  file = FileField("File", validators=[InputRequired()])
  submit = SubmitField("Upload File")

def create_file_list():
  cw=4; lottiefiles =''; n=0;

  for gallery_file in sorted(os.listdir(gallery)):
    f = os.path.join(gallery,gallery_file)
    taglist=''
    if os.path.isfile(f):
      n = (n+1)
      basename = os.path.basename(f)
      caption = deslugify(basename)
      
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

def deslugify(string):
    string = string.replace("_", " ").replace("-", " ").replace(".json", "")
    if tag_delim01 in string:
      if tag_delim02 in string:
        taglist=string[string.find(tag_delim01)+1 : string.find(tag_delim02)]
        string = string.replace(taglist, "").replace("[", "").replace("]", "")
    return string

@app.route("/")
def index():
  return render_template("index.html", body=create_file_list())

@app.route("/upload", methods=['GET','POST'])
def upload():
  form = UploadFileForm()
  if form.validate_on_submit():
    file = form.file.data
    upload_filename = form.file.data.filename
    upload_url = os.path.join(gallery,upload_filename)
    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['GALLERY'], secure_filename(file.filename)))
    message = upload_filename + ' has been uploaded.'
    return render_template("upload.html", form=form, message=message, upload_filename=upload_filename, upload_url=upload_url)

  return render_template("upload.html", form=form)

app.run(host="0.0.0.0", port=8380, debug=True)
