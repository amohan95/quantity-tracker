$(document).ready(function(){
	//get list of categories
	//ajax call to createCategoryTile off list of categories
	$.post("./API/categories", function(data){
		console.log(data);
	});
	bindEvents();
	//createCategoryTiles();
});

function bindEvents(){
	$('.tiles div').click(function(){
		if($(this).hasClass('active')){
			return;
		}
		else{
			$(this).addClass('active');
			$('.tiles div:not(.active)').fadeOut();
			$(this).css('width','95%');
			$(this).animate({
				height: "+=" + $(window).height(),
			}, 500, function(){
				//Call to get sub-classes
			});
			$(this).append($('<div>').addClass('back').html('Back').click(function(e){
					$(this).parent().removeClass('active');
					$(this).parent().css('width','20%');
					$(this).parent().animate({
						height: "-=" + $(window).height(),
					}, 500, function(){$('.tiles div:not(.active)').fadeIn();});
					$(this).remove();
					e.stopPropagation();
			}));
		}
	});
}

function createCategoryTile(data){
	return $('<div>').append($('<h3>').html(data));
}