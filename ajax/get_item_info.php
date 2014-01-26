<?php
if(isset($_GET['categoryId'])){
	class MyDB extends SQLite3
	{
		function __construct()
		{
			$this->open('../scripts/amazon/tracker.db');
		}
	}

	$db = new MyDB();

	$statement = $db->prepare('SELECT diff*price, date_time FROM listings WHERE category=:id');
	$statement->bindValue(':id', $_GET['categoryId'], SQLITE3_INTEGER);
	$result = $statement->execute();
	echo json_encode($result->fetchArray());
}
else{
	http_response_code(400);
}
?>