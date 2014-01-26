<?php
	header('Content-type: application/json');
	$db = new SQLite3('../scripts/amazon/tracker.db');
	$result = $db->query('SELECT name, id FROM categories');
	$resarr = array();
	while($row=$result->fetchArray()){
		array_push($resarr, $row);	
	}
	echo(json_encode(array("success"=>true, "categories" => $resarr)));
?>