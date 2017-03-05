<?php

$conn_string = "host=ec2-54-225-127-147.compute-1.amazonaws.com port=5432 dbname=d8vkt7mt6uqvqh user=fyjwzhtytojrxi password=c100d9cde99b45d5e4f2acefe9ef5f60438a7469da345606852f75bd60cdd6a2";
$con = pg_connect($conn_string);
if(!$con){
	echo 'Not connected to database';
	exit;
} else {
$token = $_POST['token'];
$sql = "INSERT INTO Token values ('$token')";
$result = pg_query($con, $sql);
if(!$result){
	echo "Query error.";
	exit;
}
}
pg_close($con);
echo 'Success';
?>