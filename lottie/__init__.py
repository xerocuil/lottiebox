import os
from markupsafe import escape
from flask import Flask

app = Flask(__name__)

from lottie import views
