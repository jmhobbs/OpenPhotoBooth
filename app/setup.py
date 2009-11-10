from distutils.core import setup
import py2exe

setup(
    name = 'OpenPhotoBooth',
    description = 'Free Photo Fun',
    version = '0.2',

    windows = [
                  {
                      'script': 'opb_gui.py',
                      'icon_resources': [(1, "icons/camera-photo.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      'includes': 'cairo, pango, pangocairo, atk, gobject',
                  }
              }
)