from lottie import app
from settings import LottieBoxSettings as lbs

@app.context_processor
def utility_processor():
  def get_app_title():
    return str(lbs.title)

  def get_version():
    return str(lbs.version)

  return dict(
    deslugify=deslugify,
    get_app_title=get_app_title,
    get_version=get_version
  )

def deslugify(string):
  tag_delim01 = '['
  tag_delim02 = ']'
  string = string.replace("_", " ").replace("-", " ").replace(".json", "")
  if tag_delim01 in string:
    if tag_delim02 in string:
      taglist=string[string.find(tag_delim01)+1 : string.find(tag_delim02)]
      string = string.replace(taglist, "").replace("[", "").replace("]", "")
  return string