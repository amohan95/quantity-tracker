<?php
	class MyDB extends SQLite3
	{
    	function __construct()
    	{
        	$this->open('../scripts/amazon/tracker.db');
    	}
	}
	$db = new myDB();
	$result = $db->query('SELECT name, id FROM categories');
	echo(json_encode($result));		
?>