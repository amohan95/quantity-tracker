var mongoose=require('mongoose');

var Schema = mongoose.Schema;

var productsSchema = new Schema({}});
var Products = mongoose.model('Products', productsSchema);



function Models() {
	var self = this;
	this.Prodcuts = Products;	
	var connection = mongoose.connect('mongodb://localhost/Tracker');

	mongoose.connection.once('open', function () {
		console.log("Mongodb Database Connection Established");
	  	// all set!
	})
	this.connection = connection; 
};


module.exports = new Models();
