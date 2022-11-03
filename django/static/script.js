// Load is used to ensure all images have been loaded, impossible with document

jQuery(window).load(function () {



	// Takes the gutter width from the bottom margin of .post_gallery

	var gutter = parseInt(jQuery('.post_gallery').css('marginBottom'));
	var container = jQuery('#posts_gallery');



	// Creates an instance of Masonry on #posts_gallery

	container.masonry({
		gutter: gutter,
		itemSelector: '.post_gallery',
		columnWidth: '.post_gallery'
	});
	
	
	
	// This code fires every time a user resizes the screen and only affects .post_gallery elements
	// whose parent class isn't .container. Triggers resize first so nothing looks weird.
	
	jQuery(window).bind('resize', function () {
		if (!jQuery('#posts_gallery').parent().hasClass('container')) {
			
			
			
			// Resets all widths to 'auto' to sterilize calculations
			
			post_gallery_width = jQuery('.post_gallery').width() + gutter;
			jQuery('#posts_gallery, body > #grid_gallery').css('width', 'auto');
			
			
			
			// Calculates how many .post_gallery elements will actually fit per row. Could this code be cleaner?
			
			posts_gallery_per_row = jQuery('#posts_gallery').innerWidth() / post_gallery_width;
			floor_posts_gallery_width = (Math.floor(posts_gallery_per_row) * post_gallery_width) - gutter;
			ceil_posts_gallery_width = (Math.ceil(posts_gallery_per_row) * post_gallery_width) - gutter;
			posts_gallery_width = (ceil_posts_gallery_width > jQuery('#posts_gallery').innerWidth()) ? floor_posts_gallery_width : ceil_posts_gallery_width;
			if (posts_gallery_width == jQuery('.post_gallery').width()) {
				posts_gallery_width = '100%';
			}
			
			
			
			// Ensures that all top-level elements have equal width and stay centered
			
			jQuery('#posts_gallery, #grid_gallery').css('width', posts_gallery_width);
			jQuery('#grid_gallery').css({'margin': '0 auto'});
        		
		
		
		}
	}).trigger('resize');
	


});