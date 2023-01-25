import os
class LottieBoxSettings:
  title = 'LottieBox'
  version = '0.1'
  modules = os.path.dirname(os.path.abspath(__file__))
  appdir=os.path.abspath(os.path.dirname(modules))
  user_dir=os.path.expanduser('~')
  configdir=os.path.join(user_dir,'.LottieBox')
  lb_config=os.path.join(configdir,'lb_config.ini')
