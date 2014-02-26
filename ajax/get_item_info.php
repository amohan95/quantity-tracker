<?php
if(isset($_GET['productGroup'])){
	header('Content-type: application/json');
	$db = new SQLite3('../scripts/amazon/tracker.db');
	$statement = $db->prepare("SELECT SUM(listings.change_stock*listings.price) AS revenue, date_time AS date_time
							   FROM listings JOIN items ON items.rowid=listings.item 
							   WHERE items.product_group=:id AND listings.change_stock >= 0
							   GROUP BY offer_listing_id");
	$statement->bindValue(':id', $_GET['productGroup'], SQLITE3_TEXT);
	$result = $statement->execute();
	$resarr = array();
	while($row = $result->fetchArray()){
		array_push($resarr, array('revenue' => $row['revenue'], 'datetime' => $row['date_time']));
	}
	echo json_encode(array("success"=>true, "items"=>$resarr));
}
else{
	http_response_code(400);
}
?>