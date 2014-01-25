$(document).ready(function(){
        //get list of categories
        //ajax call to createCategoryTile off list of categories
        var d = [{category:"Cats", categoryId: 1}, {category:"Dogs", categoryId: 2}, {category: "Pigs", categoryId: 3}, {category: "Canaries", categoryId: 4}];
        $.get("./API/categories", function(d){
                for(var i = 0;i<d.length;i++){
                    createCategoryTile($('#categories'), d[i]);
                }
        });
});

function createCategoryTile(tile, data){
        tile.append($('<div>').addClass('tile').append($('<h2>').html(data.category).addClass('categoryName')).data('categoryId', data.categoryId).click(function(){
                if($(this).hasClass('active')){
                        return;
                }
                else{
                        $(this).addClass('active');
                        $(this).siblings('.tile:not(.active)').fadeOut('fast');
                        var width = $(this).width();
                        var height = $(this).height();
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
                        $(this).append($('<i>').addClass('back fa fa-arrow-circle-o-left fa-3x').click(function(e){
                                $(this).parent().removeClass('active');
                                $(this).parent().animate({
                                        width: width + 5,
                                        height: height+5,
                                }, 500, function(){

                                });
                                $(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
                                $(this).parent().children(':not(.categoryName):not(.progress)').remove();
                                e.stopPropagation();
                        }));
                }
        }).append(createProgressBar('100'*1/data.categoryId,data.categoryId)));
}
function createProgressBar(percentage, id){
	return $('<div>').addClass('progress progress-striped').append($('<div>').addClass('progress-bar progress-bar-success').attr('role','progressbar')
        	.attr('aria-valuenow',percentage).attr('aria-valuemin','0').attr('aria-valuemax','100').attr('id',id).css('width', percentage + '%'));
}
function createSubCategoryTile(tile, data){
        tile.append($('<div>').addClass('tile').append($('<h3>').html(data.category).addClass('subCategoryName')).data('categoryId', data.categoryId).click(function(){
                if($(this).hasClass('active')){
                        return;
                }
                else{
                		var width = $(this).width();
                        var height = $(this).height();
                        $(this).addClass('active');
                        $(this).siblings('.tile:not(.active)').fadeOut('fast');
                        $(this).animate({
                                width: '95%',
                                height: '95%',
                        }, 500, function(){
                                //items
                                /*$.get("./API/items", function(d){
                                        for(var i = 0;i<d.length;i++){
                                                createItemTile($(this), d[i]);
                                        }
                                }*/
                        /*)*/});
                        $(this).append($('<i>').addClass('back fa fa-arrow-circle-o-left fa-3x').click(function(e){
                                $(this).parent().removeClass('active');
                                $(this).parent().animate({
                                        width: width,
                                        height: height+5,
                                }, 500, function(){

                                });
                                $(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
                                $(this).parent().children(':not(.subCategoryName):not(.progress)').remove();
                                e.stopPropagation();
                        }));
                }
        }).append(createProgressBar('100'*1/data.categoryId,data.categoryId)));
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
                                width: '95%',
                                height: "+=" + $(window).height(),
                        }, 500, function(){
                                //Item data
                                /*$.get("./API/categories", function(d){

                                }*/
                        /*)*/});
                        $(this).append($('<div>').addClass('back').html('Back').click(function(e){
                                $(this).parent().removeClass('active');
                                $(this).parent().animate({
                                        width: '25%',
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