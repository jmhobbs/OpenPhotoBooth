$( document ).ready(
	function () {
		$( document ).keypress( function ( e ) { Hook.call( 'core.onKeyPress', [ e ] ); } );
		Hook.call( 'core.onLoad', [] );
		$( window ).unload( function () { Hook.call( 'core.onUnLoad', [] ); } );
	}
);

OpenPhotoBooth = {

	capturePending: false,

	captureCallback: function ( imageData ) {
		OpenPhotoBooth.capturePending = false;

		hookArguments = []
		Hook.call( 'core.preImagePost', hookArguments );

		jQuery.ajax(
      {
			 url: "/photo",
			 dataType: 'json',
			 cache: false,
			 async: false,
			 type: "POST",
			 data: { image: imageData, hooks: hookArguments },
			 success: function ( data ) { Hook.call( 'core.postCapture', [ data ] ); }
		  }
    );

	},

	capture: function () {

		if( OpenPhotoBooth.capturePending )
			return false;

		Hook.call( 'core.preCapture', [] );

		OpenPhotoBooth.capturePending = true;

		// TEST: Cross browser working?
		if( $.browser.msie )
			document.getElementById("swf-object").capture();
		else
			document.getElementById("swf-embed").capture();
	},

	openSet: function () {

		hookArguments = []
		Hook.call( 'core.preOpenSet', hookArguments );

		jQuery.ajax(
			{
				url: "/set/open",
				dataType: 'json',
				cache: false,
				async: false,
				data: { hooks: hookArguments },
				success: function ( data ) { Hook.call( 'core.postOpenSet', [ data ] ); }
		  }
		);
	},

	closeSet: function () {

		hookArguments = []
		Hook.call( 'core.preCloseSet', hookArguments );

		jQuery.ajax(
			{
				url: "/set/close",
				dataType: 'json',
				cache: false,
				async: false,
				data: { hooks: hookArguments },
				success: function ( data ) { Hook.call( 'core.postCloseSet', [ data ] ); }
		  }
		);
	}

}