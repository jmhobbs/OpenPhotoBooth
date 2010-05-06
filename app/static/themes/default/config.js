/* OPBConfig is for all the hooks that the core.js calls */
OPBConfig = {
	// To do on loading (dom complete)
	onLoad : function () {},

	onUnload: function () {},

	// Fired when Sound Manager 2 is loaded & ready
	onSoundLoad: function () {
		OPBSkin.shutter = soundManager.createSound( {
			id: 'shutterSound',
			url: OPBSkinPath + 'shutter-short.mp3'
		} );
		OPBSkin.beep = soundManager.createSound( {
			id: 'beep',
			url: OPBSkinPath + 'beep.mp3'
		} );
	},

	// Fired immediately before a capture request is sent to the SWF
	preCapture : function () {
		OPBSkin.shutter.play();
	},

	// Fired immediately after a capture is returned from the SWF and POSTed to the server
	postCapture : function ( json ) {
		$( "#countdown" ).text( "" );
		++OPBSkin.captured;
		$( '#photo' + OPBSkin.captured ).attr( 'src', OPBThumbPath + json.thumbnail );
		if( OPBSkin.captured >= 4 ) {
			$( "#countdown" ).html( "All Done! Thanks!" );
			setTimeout( "OPBSkin.reset();", 5000 );
		}
		else
			setTimeout( "OPBSkin.countDown( 6, 1000 );", 1000 );
	},

	// Fired when a key is pressed
	onKeyPress: function (e) {
		if( e.which == 99 && ! OPBSkin.inSet ) {
			OPBSkin.inSet = true;
			OPBSkin.countDown( 6, 1000 );
		}
	},
};

/* OPBSkin is a place to safely store functions for just your skin */
OPBSkin = {
	// How many have we captured?
	captured: 0,

	// Are we "in" a set?
	inSet: false,

	// These hold soundmanager 2 sounds
	shutter: null,
	beep: null,

	countDown: function (count, interval) {
		--count;
		if(count == 0) {
			$( "#countdown" ).text( "Smile!" );
			setTimeout( "OpenPhotoBooth.capture();", 200 );
		}
		else {
			OPBSkin.beep.play();
			$( "#countdown" ).text( count );
			setTimeout("OPBSkin.countDown("+count+","+interval+");",interval);
		}
	},

	reset: function () {
	 OPBSkin.captured = 0;
	 $( "#countdown" ).text( "Welcome To OpenPhotoBooth!" );
	 OPBSkin.inSet = false;
	 for( i = 1; i <= 4; ++i ) { $( "#photo" + i ).attr( "src", OPBSkinPath + "set" + i + ".jpg"); }
	}
}
