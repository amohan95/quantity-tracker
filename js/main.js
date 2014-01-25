$(document).ready(function(){
	bindEvents();
});

function bindEvents(){
	$('.tiles div').click(function(){
		alert('help');
		$(this).css('width:80%;');
	});
}