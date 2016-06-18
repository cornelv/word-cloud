(function(){
	
	// XSRF helper
	function getCookie(name) {
	    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	    return r ? r[1] : undefined;
	}

	$(".js-scrape-form").on('submit', function(event){
		event.preventDefault();
		var url = $(".js-url").val();

		var pattern = /^(http(s)?:\/\/)?(www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;

		if(!pattern.test(url)) {
			$(".js-scrape-form").addClass('has-error');
		}
		else {
			var $btn = $(this).find('.js-scrape').button('loading');
			$(".js-scrape-form").removeClass('has-error');

			if (!url.match(/^[a-zA-Z]+:\/\//))
				url = 'http://' + url;

			// clear the old word cloud
			$(".js-word-cloud .js-word").not('.template').remove();

			$.ajax({
				url: "/scrape/",
				type: "post",
				data: {url: url, "_xsrf": getCookie("_xsrf")},
				dataType: 'json',
				success: function(data) {
					
					// insert shuffled words in DOM
					var idx = data.result.length;
					var $template = $(".js-word-cloud .js-word.template");
					var base_font_size = parseFloat($template.css('font-size'));

					while(idx--) {
						// generate a random index smaller then x
						rand_idx = Math.floor(Math.random()*(idx-1));
						if(rand_idx < 0) {
							rand_idx = 0;
						}

						// clone the template and add it to DOM
						var clone = $template.clone();
						clone.html( data.result[rand_idx][0] );
						clone.removeClass('template');
						clone.css('font-size', Math.round( base_font_size + parseFloat(data.result[rand_idx][1])/1.2));
						clone.appendTo('.js-word-cloud');

						// remove the item from array
						data.result.splice(rand_idx, 1);
					}

					$btn.button('reset');
				},
				error: function(){

					//TODO: add nice message here

					console.log(result);
				}
			});

		}

	});



})();