$(document).ready(function(){
	//get list of categories
	//ajax call to createCategoryTile off list of categories
	$.get("./API/categories", function(data){
		for(var i = 0;i<data.length;i++){
			$('.tiles').append(createCategoryTile(data[i]));
		}
	});
	bindEvents();
});

function bindEvents(){
	$('.tiles div').click(function(){
		if($(this).hasClass('active')){
			return;
		}
		else{
			$(this).addClass('active');
			$('.tiles div:not(.active)').fadeOut();
			$(this).animate({
				width: '100%',
				height: "+=" + $(window).height(),
			}, 500, function(){
				//Call to get sub-classes
			});
			$(this).append($('<div>').addClass('back').html('Back').click(function(e){
					$(this).parent().removeClass('active');
					$(this).parent().animate({
						width: '20%',
						height: '10%',
					}, 500, function(){

					});
					$(this).remove();
					$('.tiles div:not(.active)').fadeIn();
					e.stopPropagation();
			}));
		}
	});
}

function createCategoryTile(data){
	return $('<div>').append($('<h3>').html(data.category)).data('categoryId',data.categoryId);
}