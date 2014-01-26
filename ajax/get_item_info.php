<?php
if(isset($_GET['categoryId'])){
	header('Content-type: application/json');
	$db = new SQLite3('../scripts/amazon/tracker.db');
	$statement = $db->prepare('SELECT listings.change_stock*listings.price, date_time FROM listings JOIN items ON items.rowid=listings.item WHERE items.category=:id');
	$statement->bindValue(':id', $_GET['categoryId'], SQLITE3_INTEGER);
	$result = $statement->execute();
	$resarr = array();
	while($row = $result->fetchArray()){
		array_push($resarr, $row);
	}
	echo json_encode(array("success"=>true, "items"=>$result));
}
else{
	http_response_code(400);
}
?>