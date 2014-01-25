$(document).ready(function(){
	bindEvents();
});

function bindEvents(){
	$('.tiles div').click(function(){
		$(this).css('width:80%;');
	});
}