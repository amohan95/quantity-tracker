'use strict';


var db = require('../database.js'); 


exports.getProducts = function (req, res) {
	var id = req.session.account_id;
	db.Products.findOne({_id:id}, function (err, account) {
		if (err){
			res.send(err,500); 
		}else{
			res.send(account,200);  
		}
		// saved!
	})	  
};
