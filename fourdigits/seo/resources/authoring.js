$(document).ready(function () {
	$('#form-widgets-IDublinCore-title').countChars();
	$('#form-widgets-IDublinCore-description').countChars();
	$('#form-widgets-ISeo-seo_title').countChars();
	$('#form-widgets-ISeo-seo_description').countChars();
});

$.fn.extend({
	countChars: function() {
		return this.each(function() {
			$(this).setCount();
			$(this).keyup(function() {
				$(this).setCount();
			});
		})
	},
	setCount: function() {
		var id = $(this).attr('id'),
			label = $('label[for=' + id + ']'),
			text = label.html();
		text = text.trim().replace(/ \([^)]+\)/, '');
		text = text.replace(/(^\S+)/, '$1' + ' (' + $(this).val().length + ')');
		label.html(text);
	}
});