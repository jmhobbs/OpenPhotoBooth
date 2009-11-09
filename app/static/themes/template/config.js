/* OPBConfig is for all the hooks that the core.js calls */
OPBConfig = {
	// To do on loading (dom complete)
	onLoad : function () {},

	// To do on unload
	onUnload: function () {},

	// Fired when Sound Manager 2 is loaded & ready
	// Sound Manager 2 is available in the variable: "soundManager"
	onSoundLoad: function () {},

	// Fired immediately before a capture request is sent to the SWF
	preCapture : function () {},

	// Fired immediately after a capture is returned from the SWF and POSTed to the server
	// obj is the value returned from the API.
	postCapture : function ( obj ) {},

	// Fired when a key is pressed
	// e is the key event, try e.which for a # you can match on
	onKeyPress: function ( e ) {},

};

/* OPBSkin is a place to safely store functions for just your skin */
OPBSkin = {}