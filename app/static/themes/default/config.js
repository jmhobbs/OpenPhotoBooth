/* OPBConfig is for all the hooks that the core.js calls */
OPBConfig = {
	// To do on loading (dom complete)
	onLoad : function () {
		// Set up the remote controller
		//controller = window.open("", "OPB Controller", "width=150,height=30,scrollbars=no");
		//controller.document.writeln("<b>OPB Controller</b><br/><div id=\"actionarea\"><a href=\"javascript:opener.OPBSkin.getASet();\">Start Capture</a></div>");
	},

	onUnload: function () {
    //controller.close();
  },

	// Fired when Sound Manager 2 is loaded & ready
	onSoundLoad: function () {
		OPBSkin.shutter = soundManager.createSound( {
			id: 'shutterSound',
			url: OPBSkinPath + 'shutter-short.mp3'
		} );
	},

	// Fired immediately before a capture request is sent to the SWF
	preCapture : function () {
		OPBSkin.shutter.play();
	},

	// Fired immediately after a capture is returned from the SWF and POSTed to the server
	postCapture : function ( json ) {
		$( "#countdown" ).html("");
		++OPBSkin.captured;
		$( '#photo' + OPBSkin.captured ).attr( 'src', json.thumbpath );
		if( OPBSkin.captured >= 4 ) {
			$("#countdown").html("All Done! Thanks!");
			setTimeout("OPBSkin.reset();",5000);
			//controller.document.getElementById("actionarea").innerHTML = "<a href=\"javascript:opener.OPBSkin.getASet();\">Start Capture</a>";
		}
		else
			setTimeout("OPBSkin.countDown(6,1000);",1000);
	},

	// Fired before a request is sent to the server for a new set
	preStartSet : function () {},

	// Fired after the server gives us a new set
	postStartSet : function ( json ) {
    setTimeout("OPBSkin.countDown(6,1000);",1000);
  },

	// Fired before asking the server to end the current set
	preEndSet : function () {},

	// Fired after the server has ended the current set
	postEndSet : function () {},

	// Fired when a key is pressed
	onKeyPress: function (e) {
		if(e.which == 99 && !OpenPhotoBooth.capturePending)
			OPBSkin.getASet();
	},
};

/* OPBSkin is a place to safely store functions for just your skin */
OPBSkin = {
	captured: 0,
	shutter: null,

	countDown: function (count, interval) {
		--count;
		if(count == 0) {
			$("#countdown").html("Smile!");
			setTimeout('OpenPhotoBooth.capture();',200);
		}
		else {
			$("#countdown").html(count);
			setTimeout("OPBSkin.countDown("+count+","+interval+");",interval);
		}
	},

	getASet: function () {
		controller.document.getElementById("actionarea").innerHTML = "Please Wait";
		OPBSkin.captured = 0;
		OpenPhotoBooth.startSet();
	},

	reset: function () {
	 $("#countdown").html("");
	 for(i = 1; i <= 4; ++i)
	   $('#photo'+i).attr('src','skins/default/set'+i+'.jpg');
	}
}