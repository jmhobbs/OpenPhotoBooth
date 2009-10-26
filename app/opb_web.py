# -*- coding: utf-8 -*-

"""
Copyright (c) 2009 Little Filament

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

#render = web.template.render( 'template/' )
app = web.application( urls, globals() )

class main:
	def GET( self ):
		""" Bounce them to the static template index.html """
		raise web.redirect( '/static/index.html' )

class save_photo:
	def POST( self ):
                web.header( 'Content-type', 'application/json; charset=utf-8' )
                
                """ Save the photo data, thumbnail it and move on. """
		i = web.input( image=None )
		
		filename = "%s.jpg" % ( time.time() )
		
		fullsize = open( './photos/' + filename, 'wb' )
		fullsize.write( base64.standard_b64decode( i.image ) )
		fullsize.close()
		
		size = 160, 120
		im = Image.open( './photos/' + filename )
		im.thumbnail( size )
		im.save( './thumbs/' + filename, "JPEG" )
		return '{ "saved": true, "thumbnail": "%s" }' % ( filename )

class favicon_serve:
  def GET ( self ):
    raise web.redirect( '/static/favicon.ico' )

if __name__ == "__main__" :
	app.run()
