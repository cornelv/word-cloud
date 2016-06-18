(function(){
	
	// XSRF helper
	function getCookie(name) {
	    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	    return r ? r[1] : undefined;
	}

	$(".js-scrape").on('click', function(event){
		event.preventDefault();
		var url = $(".js-url").val();

		var pattern = /^(http(s)?:\/\/)?(www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;

		if(!pattern.test(url)) {
			$(".js-scrape-form").addClass('has-error');
		}
		else {
			var $btn = $(this).button('loading');
			$(".js-scrape-form").removeClass('has-error');
			$.ajax({
				url: "/scrape/",
				type: "post",
				data: {url: url, "_xsrf": getCookie("_xsrf")},
				success: function(result) {
					console.log(result);
					$btn.button('reset')
				},
			});

		}

	});

})();