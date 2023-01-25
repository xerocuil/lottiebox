import os
from markupsafe import escape
from flask import Flask
from settings import LottieBoxSettings as lbs

lottiebox = Flask(__name__,
  static_url_path='/static', 
  static_folder='static',
  template_folder='templates'
)

from lottie import views
