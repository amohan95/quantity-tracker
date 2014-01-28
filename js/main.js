$(document).ready(function(){
        //get list of categories
        //ajax call to createCategoryTile off list of categories
        $.get("./ajax/get_categories.php", function(d){
            for(var i = 0;i<d.categories.length;i++){
                createCategoryTile($('#categories'), d.categories[i]);
            }
        });
        searchTiles();
    });

function searchTiles(){
	$('#categorySearch').on('input', function() {
		if(!$('#categorySearch')) return;
		$.each($('.categoryName'), function(key, head){
			var search = $('#categorySearch').val().toLowerCase();
			var head_val = $(head).text().toLowerCase();
			if(!(head_val.indexOf(search) >= 0)) $(head).parent().fadeOut();
			else $(head).parent().fadeIn();
		}
       )});
	$('#subCategorySearch').on('input', function(){
		$.each($('.subCategoryName'), function(key, head){
			var search = $('#subCategorySearch').val().toLowerCase();
			var head_val = $(head).text().toLowerCase();
			if(!(head_val.indexOf(search) >= 0)) $(head).parent().fadeOut();
			else $(head).parent().fadeIn();
		}
       )
	});
}

function createCategoryTile(tile, data){
    var categoryTile = $('<div>').addClass('tile').append($('<h2>').html(data.name).addClass('categoryName')).attr('data-categoryId', data.id);
    tile.append(categoryTile.click(function(){
        if($(this).hasClass('active')){
            return;
        }
        else{
            $(this).addClass('active');
            $(this).siblings('.tile:not(.active)').fadeOut('fast');
            var width = $(this).width();
            var height = $(this).height();
            $(this).animate({
                width: '95%',
                height: "+=" + $(window).height(),
            }, 500, function(){
              //create subcategories 

              $.get("./ajax/get_subcategories.php", {"categoryId" : data.id}, function(d){
                for(var i = 0;i<d.categories.length;i++){
                    createSubCategoryTile(categoryTile, d.categories[i]);
                }
            }
            )});
            $('#categorySearch').attr('id','subCategorySearch').off();
            $('#subCategorySearch').val('');
            searchTiles();
            $(this).append($('<i>').addClass('back fa fa-arrow-circle-o-left fa-3x').click(function(e){
                $(this).parent().removeClass('active');
                $('#subCategorySearch').attr('id','categorySearch').off();
                $('#categorySearch').val('');
                $('#categorySearch').prop('disabled', false);
                searchTiles();
                $(this).parent().animate({
                    width: width + 5,
                    height: height + 9,
                }, 500, function(){

                });
                $(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
                $(this).parent().children(':not(.categoryName):not(.progress)').remove();
                e.stopPropagation();
            }));
        }
    }));
}
function createProgressBar(percentage, id){
	return $('<div>').addClass('progress progress-striped').append($('<div>').addClass('progress-bar progress-bar-success').attr('role','progressbar')
       .attr('aria-valuenow',percentage).attr('aria-valuemin','0').attr('aria-valuemax','100').attr('id',id).css('width', percentage + '%'));
}
function createSubCategoryTile(tile, data){
    tile.append($('<div>').addClass('tile').append($('<h3>').html(data.name).addClass('subCategoryName')).attr('data-categoryId', data.id).click(function(){
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

        });
          var plotPoints = [];
          var yMax = 0;
            $('.active > .subCategoryName').append($('<div>').attr('class','graph-wrapper').append($('<div>').attr('id','placeholder').css('width','800px').css('height','400px')));
            var plot = $.plot($('#placeholder'), [[12, 42], [14,54]], { yaxis: { max: yMax, min: 0 } });
          var jqxhr = $.get("./ajax/get_item_info.php", {'categoryId': data.id}, function(d){
            for(var i = 0;i<d.items.length;i++){
                if(d.items[i][1] > yMax) yMax = d.items[i][1]*1.1;
                plotPoints.push(d.items[i]);
            }
        }).done(function(){
            console.log(plotPoints);
            // plot.setData(plotPoints);
            // plot.draw();
        }).fail(function(){

        }).always(function(){

        });
        $('#subCategorySearch').prop('disabled', true);
        $(this).append($('<i>').addClass('back fa fa-arrow-circle-o-left fa-3x').click(function(e){
            $('.graph-wrapper').remove();
            $(this).parent().removeClass('active');
            $(this).parent().animate({
                width: width,
                height: height+5,
            }, 500, function(){

            });
            $(this).parent().siblings('.tile:not(.active)').fadeIn('slow');
            $(this).parent().children(':not(.subCategoryName)').remove();
            $('#subCategorySearch').prop('disabled', false);
            e.stopPropagation();
        }));
    }
}));
}