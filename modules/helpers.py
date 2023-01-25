import os
from settings import LottieBoxSettings as lbs
from configparser import ConfigParser
from lottie import lottiebox

# Read lb_config.ini file
lottiebox_config = ConfigParser()
lottiebox_config.read(lbs.lb_config)

gallery=os.path.abspath(lottiebox_config['USERCONFIG']['lottiefiles'])

# if not os.path.exists(gallery):
#   os.makedirs(gallery)

tag_delim01 = '['; tag_delim02 = ']';

@lottiebox.context_processor
def utility_processor():
  def get_app_title():
    return str(lbs.title)

  def get_tag_arr():
    tags_all = []
    for gallery_file in sorted(os.listdir(gallery)):
      j = os.path.join(gallery,gallery_file)
      if os.path.isfile(j):
        if tag_delim01 in j:
          if tag_delim02 in j:
            if j.find(tag_delim01) > j.find(tag_delim02):
              continue
            else:
              tag_str = j[j.find(tag_delim01)+1 : j.find(tag_delim02)]
              tag_arr = tag_str.split(",")
              if tag_arr[0] == '':
                continue
              else:
                tags_all.extend(tag_arr)

    tags = sorted(list(set(tags_all)))
    return tags

  def get_version():
    return str(lbs.version)

  def row_split(colwidth,index):
    if index % colwidth == 0:
      row_split=True
      return row_split

  def set_autoplay():
    if lottiebox_config['USERCONFIG']['autoplay'] == "True":
      autoplay='autoplay'
    else:
      autoplay='hover'
    return autoplay

  return dict(
    get_app_title=get_app_title,
    get_tag_arr=get_tag_arr,
    get_version=get_version,
    row_split=row_split,
    set_autoplay=set_autoplay
  )

def deslugify(string):
  string = string.replace("_", " ").replace("-", " ").replace(".json", "")
  if tag_delim01 in string:
    if tag_delim02 in string:
      taglist=string[string.find(tag_delim01)+1 : string.find(tag_delim02)]
      string = string.replace(taglist, "").replace("[", "").replace("]", "")
  return string


