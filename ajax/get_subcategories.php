<?php

if(isset($_GET['categoryId'])){
	header('Content-type: application/json');
	$db = new SQLite3('../scripts/amazon/tracker.db');
	$statement = $db->prepare('SELECT name, id FROM subcategories WHERE parent=:id');
	$statement->bindValue(':id', $_GET['categoryId'], SQLITE3_INTEGER);
	$result = $statement->execute();
	$resarr = array();
	while($row = $result->fetchArray()){
		array_push($resarr, $row);
	}
	echo(json_encode(array("success"=>true, "categories" => $resarr)));
}
else{
	http_response_code(400);
}		
?>