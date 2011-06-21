
class Plugin:

	def GET ( self, path, web, app ):
		return ''.join( ( '<h1>', 'Hello ', path, '!</h1>' ) )
	
	def POST ( self, path, web, app ):
		return '<h1>Hi!</h1>';

