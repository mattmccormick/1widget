$(document).ready(function() {
	$("form").submit(function() {
		$("form input[type='submit']").attr('disabled','disabled');
	});
});
