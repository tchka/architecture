$(document).ready(function(){
	// Header Menu

	$(function() {
		var pull = $('.hamburger');
		var menu = $('.main-nav');

		$(pull).on('click', function(e) {
			e.preventDefault();
			menu.toggleClass('open');
			pull.toggleClass('is-active');
		});

		$(window).resize(function(){
			var w = $(window).width();
			if(w > 1116 && menu.is(':hidden')) {
				menu.removeClass('open');
				pull.removeClass('is-active');
			}
		});

		$('body').click(function (event) {
			var w = $(window).width();
			if((w < 1117) && ($(event.target).closest(".main-nav").length === 0) && ($(event.target).closest(".hamburger").length === 0)) {
				$(".hamburger").removeClass('is-active');
				$(".main-nav").removeClass('open');
			}
		});
	});	

	
});