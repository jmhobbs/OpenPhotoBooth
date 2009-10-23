$(document).ready(function () {
	$(document).keypress(function(e) { OPBConfig.onKeyPress(e); });
	OPBConfig.onLoad();
});

$(window).unload(function () { OPBConfig.onUnLoad() });

OpenPhotoBooth = {
	// Flag to see if we are currently asking the SWF for an image
	capturePending: false,

	captureCallback: function (imageData) {
		OpenPhotoBooth.capturePending = false;

		jQuery.ajax(
      {
			 url: "/photo",
			 dataType: 'json',
			 cache: false,
			 async: false,
			 type: "POST",
			 data: {image: imageData},
			 success: function (data) { OPBConfig.postCapture(data); }
		  }
    );

	}, /* End captureCallback() */

	capture: function () {

		if(OpenPhotoBooth.capturePending)
			return false;

		OPBConfig.preCapture();

		OpenPhotoBooth.capturePending = true;

		// TEST: Cross browser working?
		if( $.browser.msie )
			document.getElementById("swf-object").capture();
		else
			document.getElementById("swf-embed").capture();
	}

} /* End OpenPhotoBooth */