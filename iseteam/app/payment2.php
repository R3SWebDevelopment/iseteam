<?php
require_once __DIR__.'/vendor/autoload.php';
\Conekta\Conekta::setApiKey('key_3jSBxMareZQRRv1PoJaWzw');
\Conekta\Conekta::setLocale('en');

$response = array();
$conn_string = "host=ec2-54-225-127-147.compute-1.amazonaws.com port=5432 dbname=d8vkt7mt6uqvqh user=fyjwzhtytojrxi password=c100d9cde99b45d5e4f2acefe9ef5f60438a7469da345606852f75bd60cdd6a2";
$con = pg_connect($conn_string);
if(!$con){
	echo 'Not connected to database';
	exit;
} else {

$token = $_POST['token'];
$name = $_POST['name'];
$email = $_POST['email'];
$phone = $_POST['phone'];
$id = $_POST['eventId'];

$sql = "SELECT * FROM Event WHERE (idEvent = $id)";
$result = pg_query($con, $sql);
if(!$result){
	echo 'Query error';
	exit;
} else {
$row = pg_fetch_row($result);
$title = $row[1];
$cost = $row[4];

try{
	$charge = Conekta\Charge::create(array(
	  'description'=> "$title",
	  'amount'=> $cost*100,
	  'currency'=>'MXN',
	  'card'=> "$token",
	  'details'=> array(
		'name'=> "$name",
		'phone'=> "$phone",
		'email'=> "$email",
		'line_items'=> array(
		  array(
			'name'=> "$title",
			'description'=> "$title",
			'unit_price'=> $cost*100,
			'quantity'=> 1,		       
			'type'=> 'event'
		  )
		)
	  )
	));
	if($charge->status == 'paid'){
		$response['success'] = 1;
		$response['message'] = "Purchase successful";
		echo json_encode($response);
	}
} catch (Conekta\Error $e) {
	$response['success'] = 0;
	$response['message'] = $e->message_to_purchaser;
	echo json_encode($response);
}
}
}
?>