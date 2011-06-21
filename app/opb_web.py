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
import os
import mimetypes

mimetypes.init()


web.config.debug = False

urls = [
	'/', 'main',
	'/set/open', 'open_set',
	'/set/close', 'close_set',
	'/photo', 'save_photo',
  '/favicon.ico', 'favicon_serve',
	'/plugin/(.*)/static/(.*)', 'plugin_static',
	'/plugin/(.*)/(.*)', 'plugin_serve',
]

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

theme_render = None
set_id = False

##### Load Plugins
requested_plugins = [ 'hello_world', ]
plugins = {}

for name in requested_plugins:
	m = __import__( '.'.join( ( 'plugins', name ) ), [], [], ['hook'], -1 )
	plugins[name] = m.hook.Plugin()
##### End Plugins

# Sets everything required for properly rendering a theme
def SetTheme ( theme_name ):
	global theme_render
	global opb
	opb['theme_path'] = '/static/themes/%s/' % ( theme_name )
	theme_render = web.template.render( 'static/themes/%s/' % ( theme_name ) )

# Create the application
app = web.application( tuple( urls ), globals() )

class main:
	def GET( self ):
		return theme_render.index( opb )

# Serves static files at /plugin/[plugin name]/[file path]
class plugin_static:
	def GET ( self, plugin, path ):
		filename = os.path.join( 'plugins', plugin, 'static', path ) 
		if os.path.isfile( filename ):
			t = mimetypes.guess_type( filename )
			if t[0]:
				web.header( 'Content-Type', t[0] )
				web.header('Transfer-Encoding','chunked') 
				with open( filename, 'rb' ) as f: 
					while 1:
						buf = f.read(1024 * 8) 
						if not buf: 
							break 
						yield buf
				return
		
		app.notfound()

class plugin_serve:
	def GET ( self, plugin, path ):
		if plugin in plugins.keys():
			return plugins[plugin].GET( path, web, app )
		else:
			app.notfound()
	def POST ( self, plugin, path ):
		if plugin in plugins.keys():
			return plugins[plugin].POST( path, web, app )
		else:
			app.notfound()

class save_photo:
	def POST( self ):
		global set_id
		web.header( 'Content-type', 'application/json; charset=utf-8' )

		""" Save the photo data, thumbnail it and move on. """
		i = web.input( image=None )

		if False != set_id:
			filename = "%s_%s.jpg" % ( set_id, int( time.time() ) )
		else:
			filename = "NOSET_%s.jpg" % ( int( time.time() ) )

		fullsize = open( './static/photos/' + filename, 'wb' )
		fullsize.write( base64.standard_b64decode( i.image ) )
		fullsize.close()

		size = 160, 120
		im = Image.open( './static/photos/' + filename )
		im.thumbnail( size )
		im.save( './static/thumbs/' + filename, "JPEG" )
		return '{ "saved": true, "thumbnail": "%s" }' % ( filename )

class open_set:
	def GET ( self ):
		global set_id
		set_id = "%s" % int( time.time() )
		return '{ "set": "%s" }' % set_id

class close_set:
	def GET ( self ):
		global set_id
		set_id = False
		return '{ "set": false }'

class favicon_serve:
	def GET ( self ):
		raise web.redirect( '/static/favicon.ico' )

if __name__ == "__main__" :
	SetTheme( 'default' )
	app.run()
