var mongoose=require('mongoose');

var Schema = mongoose.Schema;

var itemsSchema = new Schema({name : {type: String, default: null},asin : {type: String, default: null},category: {type: String, default: null},rank : {type: Number, default: null},price : {type: Number, default: null},shipping : {type: Number, default: null}});
var Items = mongoose.model('Items', itemsSchema);

var listingsSchema = new Schema({offer_listing_id : {type: String, default: null},price : {type: Number, default: null},shipping : {type: Number, default: null},current_stock : {type: Number, default: null}});
var Listings = mongoose.model('Listings', listingsSchema);


function Models() {
	var self = this;
	this.Items = Items;	
	this.Listings = Listings;	
	var connection = mongoose.connect('mongodb://localhost/Tracker');

	mongoose.connection.once('open', function () {
		console.log("Mongodb Database Connection Established");
	  	// all set!
	})
	this.connection = connection; 
};


module.exports = new Models();
