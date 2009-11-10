# -*- coding: utf-8 -*-

"""
Copyright (c) 2009 John Hobbs, Little Filament

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import web
import Image
import base64
import time

web.config.debug = False

urls = (
	'/', 'main',
	'/photo', 'save_photo',
  '/favicon.ico', 'favicon_serve'
)

# Need a render engine for the core template files
core_render = web.template.render( 'static/core/' )
# Now make that available to the template engine as a global
web.template.Template.globals['core'] = core_render

# A configuration object to pass information to themes
opb = {
	'core_path': '/static/core/',
	'vendor_path': '/static/vendor/',
	'theme_path': '/static/themes/default/',
  'thumb_path': '/static/thumbs/'
}

global theme_render
theme_render = None

# Sets everything required for properly rendering a theme
def SetTheme ( theme_name ):
	global theme_render
	global opb
	opb['theme_path'] = '/static/themes/%s/' % ( theme_name )
	theme_render = web.template.render( 'static/themes/%s/' % ( theme_name ) )

# Create the application
app = web.application( urls, globals() )

class main:
	def GET( self ):
		return theme_render.index( opb )

class save_photo:
	def POST( self ):
		web.header( 'Content-type', 'application/json; charset=utf-8' )

		""" Save the photo data, thumbnail it and move on. """
		i = web.input( image=None )

		filename = "%s.jpg" % ( time.time() )

		fullsize = open( './static/photos/' + filename, 'wb' )
		fullsize.write( base64.standard_b64decode( i.image ) )
		fullsize.close()

		size = 160, 120
		im = Image.open( './static/photos/' + filename )
		im.thumbnail( size )
		im.save( './static/thumbs/' + filename, "JPEG" )
		return '{ "saved": true, "thumbnail": "%s" }' % ( filename )

class favicon_serve:
	def GET ( self ):
		raise web.redirect( '/static/favicon.ico' )

if __name__ == "__main__" :
	SetTheme( 'default' )
	app.run()