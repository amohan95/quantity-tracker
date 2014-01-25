'use strict';


var db = require('../database.js'); 
var mongoose = require('mongoose');

exports.getItems = function (req, res) {

	db.Items.find({}, function (err, items) {
		if (err){
			res.send(err,500); 
		}else{
			res.send(items,200);  
		}
		// saved!
	})	  
};

exports.getCategories = function (req, res) {
	var categories = [{category:'Fun and Games',revenue:9023,categoryId:mongoose.Types.ObjectId()},{category:'Auto',revenue:9023,categoryId:mongoose.Types.ObjectId()},{category:'Sports',revenue:9023,categoryId:mongoose.Types.ObjectId()}];
	
	res.send(categories);
};
/*
exports.getCategories = function (req, res) {
	var catagories = [{catagory:'Fun and Games',revenue:9023},{catagory:'Auto',revenue:9023},{catagory:'Sports',revenue:9023}];
	
	res.send(catagories);
};
*/

