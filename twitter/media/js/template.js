$(document).ready(function() {
	$("#toggle").click(function() {
		$("#tips").toggle('normal');
		var text = '(hide)';
		if ($(this).text() == text) {
			text = '(show)';
		}
		
		$(this).text(text);
		return false;
	});
});