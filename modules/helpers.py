import os
from settings import LottieBoxSettings as lbs
from configparser import ConfigParser

from lottiebox import lottiebox

## Load config
lottiebox_config = ConfigParser()
lottiebox_config.read(lbs.lb_config)
gallery=os.path.abspath(lottiebox_config['USERCONFIG']['lottiefiles'])
tag_delim01 = '['; tag_delim02 = ']';

## Template Tags
@lottiebox.context_processor
def utility_processor():
  def get_app_title():
    return str(lbs.title)

  def get_tags(filename):
    file_tags = []
    if tag_delim01 in filename:
      if tag_delim02 in filename:
        if filename.find(tag_delim01) > filename.find(tag_delim02):
          print('No tags')
        else:
          tag_str = filename[filename.find(tag_delim01)+1 : filename.find(tag_delim02)]
          tag_arr = tag_str.split(",")
          
          if tag_arr[0] == '':
            print('No tags')
          else:
            file_tags = tag_arr
    return file_tags

  def get_tag_arr():
    tags_all = []
    for gallery_file in sorted(os.listdir(gallery)):
      f = os.path.join(gallery,gallery_file)
      if os.path.isfile(f):
        tags = get_tags(gallery_file)
        if tags:
          tags_all.extend(tags)

    tag_list = sorted(list(set(tags_all)))
    return tag_list

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
    get_tags=get_tags,
    get_version=get_version,
    row_split=row_split,
    set_autoplay=set_autoplay
  )

## Shared Functions
def deslugify(string):
  string = string.replace("_", " ").replace("-", " ").replace(".json", "")
  if tag_delim01 in string:
    if tag_delim02 in string:
      taglist=string[string.find(tag_delim01)+1 : string.find(tag_delim02)]
      string = string.replace(taglist, "").replace("[", "").replace("]", "")
  return string

def get_tags2(filename):
  file_tags = []
  if tag_delim01 in filename:
    if tag_delim02 in filename:
      if filename.find(tag_delim01) > filename.find(tag_delim02):
        print('No tags')
      else:
        tag_str = filename[filename.find(tag_delim01)+1 : filename.find(tag_delim02)]
        tag_arr = tag_str
        
        if tag_arr[0] == '':
          print('No tags')
        else:
          file_tags = tag_arr
  return file_tags

def sizeof_fmt(num, suffix="B"):
  for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Yi{suffix}"