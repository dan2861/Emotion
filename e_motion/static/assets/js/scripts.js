
function scroll_to(clicked_link, nav_height) {
	var element_class = clicked_link.attr('href').replace('#', '.');
	var scroll_to = 0;
	if(element_class != '.top-content') {
		element_class += '-container';
		scroll_to = $(element_class).offset().top - nav_height;
	}
	if($(window).scrollTop() != scroll_to) {
		$('html, body').stop().animate({scrollTop: scroll_to}, 1000);
	}
}


jQuery(document).ready(function() {
	
	/*
	    Navigation
	*/
	$('a.scroll-link').on('click', function(e) {
		e.preventDefault();
		scroll_to($(this), $('nav').outerHeight());
	});
	// toggle "navbar-no-bg" class
	$('.top-content h1').waypoint(function() {
		$('nav').toggleClass('navbar-no-bg');
	});
	
    /*
        Background slideshow
    */
	$('.top-content').backstretch("static/assets/img/backgrounds/1.jpg");
    $('.section-4-container').backstretch("static/assets/img/backgrounds/2.jpg");
    
    /*
	    Wow
	*/
	new WOW().init();

	/*
		LogIn
	*/
	$('.login-info-box').fadeOut();
    $('.login-show').addClass('show-log-panel');
});

/* Login/Reg Button */
$('.login-reg-panel input[type="radio"]').on('change', function() {
    if($('#log-login-show').is(':checked')) {
        $('.register-info-box').fadeOut(); 
        $('.login-info-box').fadeIn();
        
        $('.white-panel').addClass('right-log');
        $('.register-show').addClass('show-log-panel');
        $('.login-show').removeClass('show-log-panel');
        
    }
    else if($('#log-reg-show').is(':checked')) {
        $('.register-info-box').fadeIn();
        $('.login-info-box').fadeOut();
        
        $('.white-panel').removeClass('right-log');
        
        $('.login-show').addClass('show-log-panel');
        $('.register-show').removeClass('show-log-panel');
    }
});


function sendVideoWatchEvent(videoid) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", '/watchevent', true);

	//Send the proper header information along with the request
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	xhr.send("videoid="+videoid);
}

// Src: https://stackoverflow.com/questions/37360365/jquery-click-for-video-element
/* Video Click Event */
$("video.embed-responsive-item").on("play", function (e) {
	console.log("Video play event for id: " + e.target.id);
	sendVideoWatchEvent(e.target.id);
});

// Src: https://github.com/vincepare/iframeTracker-jquery#advanced-tracking
/* Iframe Click Event */
jQuery(document).ready(function($){
	$('iframe.embed-responsive-item').iframeTracker({
		blurCallback: function(event) {
			// Do something when iframe is clicked (like firing an XHR request)
			// You can know which iframe element is clicked via this._overId
			console.log("Iframe play event for id: " + this._overId);
			sendVideoWatchEvent(this._overId);
		},
		overCallback: function(element, event) {
			this._overId = $(element).attr('id'); // Saving the iframe id
		},
		outCallback: function(element, event) {
			this._overId = null; // Reset hover iframe wrapper id
		},
		_overId: null
	});
});
