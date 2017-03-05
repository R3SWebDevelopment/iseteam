<?php
$conn_string = "host=ec2-54-225-127-147.compute-1.amazonaws.com port=5432 dbname=d8vkt7mt6uqvqh user=fyjwzhtytojrxi password=c100d9cde99b45d5e4f2acefe9ef5f60438a7469da345606852f75bd60cdd6a2";
$con = pg_connect($conn_string);
if(!$con){
	echo 'Not connected to database';
	exit;
} else {
 $body = @file_get_contents('php://input');
$event_json = json_decode($body);
if ($event_json->type == 'charge.paid'){
 //Hacer algo con la información como actualizar los atributos de la orden en tu base de datos
 $name = $event_json->data->object->details->name;
 $description = $event_json->data->object->description;
 $email = $event_json->data->object->details->email;
 $dtString = date("Y/m/d");
$sql = "INSERT INTO payment (name, email, event, date) values ('$name', '$email', '$description', '$dtString')";
$result = pg_query($con, $sql);
if(!$result){
	echo "Query error.";
	exit;
} else {
	http_response_code(200);
}
pg_close($con);
}
}
?>