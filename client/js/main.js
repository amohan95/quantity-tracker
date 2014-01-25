$(document).ready(function(){
	//get list of categories
	//ajax call to createCategoryTile off list of categories
	$.get("./API/categories", function(data){
		for(var i = 0;i<data.length;i++){
			$('#categories').append(createCategoryTile(data[i]));
		}
		});
});

function createCategoryTile(data){
	var tile = $('<div>').addClass('tile').append($('<h2>').html(data.category).addClass('categoryName')).data('categoryId', data.categoryId).click(function(){
		if($(this).hasClass('active')){
			return;
		}
		else{
			$(this).addClass('active');
			$(this).siblings('.tile:not(.active)').fadeOut('fast');
			$(this).animate({
				width: '98%',
				height: "+=" + $(window).height(),
			}, 500, function(){
				//subcategories
				$.get("./API/categories", function(d){
					for(var i = 0;i<d.length;i++){
						createSubCategoryTile($(this), d[i]);
					}
				}
			)});
			$(this).append($('<div>').addClass('back').html('Back').click(function(e){
				$(this).parent().removeClass('active');
				$(this).parent().animate({
					width: '20%',
					height: '10%',
				}, 500, function(){

				});
				$(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
				$(this).parent().children(':not(.categoryName)').remove();
				e.stopPropagation();
			}));
		}
	});
	return tile;
}

function createSubCategoryTile(tile, data){
	tile.append($('<div>').addClass('tile').append($('<h3>').html(data.category).addClass('subCategoryName')).data('categoryId', data.categoryId).click(function(){
		if($(this).hasClass('active')){
			return;
		}
		else{
			$(this).addClass('active');
			$(this).siblings('.tile:not(.active)').fadeOut('fast');
			$(this).animate({
				width: '98%',
				height: "+=" + $(window).height(),
			}, 500, function(){
				//items
				$.get("./API/categories", function(d){
					for(var i = 0;i<d.length;i++){
						createItemTile($(this), d[i]);
					}
				}
			)});
			$(this).append($('<div>').addClass('back').html('Back').click(function(e){
				$(this).parent().removeClass('active');
				$(this).parent().animate({
					width: '20%',
					height: '10%',
				}, 500, function(){

				});
				$(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
				$(this).parent().children(':not(.subCategoryName)').remove();
				e.stopPropagation();
			}));
		}
	}));
}

function createItemTile(tile, data){
	tile.append($('<div>').addClass('tile').append($('<h4>').html(data.category).addClass('subCategoryName')).data('categoryId', data.categoryId).click(function(){
		if($(this).hasClass('active')){
			return;
		}
		else{
			$(this).addClass('active');
			$(this).siblings('.tile:not(.active)').fadeOut('fast');
			$(this).animate({
				width: '98%',
				height: "+=" + $(window).height(),
			}, 500, function(){
				//Item data
				$.get("./API/categories", function(d){

				}
			)});
			$(this).append($('<div>').addClass('back').html('Back').click(function(e){
				$(this).parent().removeClass('active');
				$(this).parent().animate({
					width: '20%',
					height: '5%',
				}, 500, function(){

				});
				$(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
				$(this).parent().children(':not(.subCategoryName)').remove();
				e.stopPropagation();
			}));
		}
	}));
}