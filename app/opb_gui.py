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

import pygtk
pygtk.require( '2.0' )
import gtk

from multiprocessing import Process

import opb_web

import webbrowser

############## gtk Stuff ##############

def server_process ():
	opb_web.app.run()

class OPB_UI:

	def start( self, widget, data=None ):
		self.process = Process( target=server_process, args=() )
		self.process.start()
		self.stop_button.set_sensitive( True )
		self.start_button.set_sensitive( False )
		self.browser_button.set_sensitive( True )
		# Windows barfs on the <a></a> tag, so no nice browser opening :(
		self.status_label.set_text( 'Open browser to http://localhost:8080/' )

	def destroy( self, widget, data=None ):
		self.stop( widget, data )
		gtk.main_quit()

	def stop( self, widget, data=None ):
		if None != self.process:
			self.process.terminate()
			self.stop_button.set_sensitive( False )
			self.browser_button.set_sensitive( False )
			self.start_button.set_sensitive( True )
			self.status_label.set_text( 'Click "Start" To Run Server' )

	def about ( self, widget, data=None ):
		dialog = gtk.AboutDialog()

		dialog.set_program_name( 'OpenPhotoBooth' )
		dialog.set_version( '0.1' )
		dialog.set_website( 'http://www.openphotobooth.com/' )
		dialog.set_copyright( '(c) 2009 Little Filament' )
		dialog.set_authors( [ 'John Hobbs - admin@littlefilament.com', '', 'Server by web.py', 'GUI by pygtk', 'jQuery' ] )
		dialog.set_comments( 'Free Photo Fun' )

		dialog.run()
		dialog.hide()

	def __init__( self ):
		self.process = None;

		self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
		self.window.connect( "destroy", self.destroy)
		self.window.set_border_width( 10 )
		self.window.set_title( 'OpenPhotoBooth Control' )
		self.window.resize( 300, 1 )

		table = gtk.Table( 3, 2, True )

		self.status_label = gtk.Label( 'Click "Start" To Run Server' )
		table.attach( self.status_label, 0, 2, 0, 1 )
		self.status_label.show()

		self.start_button = gtk.Button( "Start" )
		self.start_button.connect( "clicked", self.start, None )
		self.start_button.set_image( gtk.image_new_from_file( 'icons/media-playback-start.png' ) )
		table.attach( self.start_button, 0, 1, 1, 2 )
		self.start_button.show()

		self.stop_button = gtk.Button( "Stop" )
		self.stop_button.connect( "clicked", self.stop, None )
		self.stop_button.set_sensitive( False )
		self.stop_button.set_image( gtk.image_new_from_file( 'icons/media-playback-stop.png' ) )
		table.attach( self.stop_button, 1, 2, 1, 2 )
		self.stop_button.show()
		
		about_button = gtk.Button( "About" )
		about_button.connect( "clicked", self.about, None )
		about_button.set_image( gtk.image_new_from_file( 'icons/help-browser.png' ) )
		table.attach( about_button, 0, 1, 2, 3 )
		about_button.show()

		quit_button = gtk.Button( "Quit" )
		quit_button.connect( "clicked", self.destroy, None )
		quit_button.set_image( gtk.image_new_from_file( 'icons/process-stop.png' ) )
		table.attach( quit_button, 1, 2, 2, 3 )
		quit_button.show()

		self.window.add( table )

		table.show()
		self.window.show()

	def main( self ):
		gtk.main()

if __name__ == "__main__":

	gtk.window_set_default_icon_from_file( 'icons/camera-photo.png' )

	opb_ui = OPB_UI()
	opb_ui.main()