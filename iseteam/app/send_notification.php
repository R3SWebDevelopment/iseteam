<?php
$conn_string = "host=ec2-54-225-127-147.compute-1.amazonaws.com port=5432 dbname=d8vkt7mt6uqvqh user=fyjwzhtytojrxi password=c100d9cde99b45d5e4f2acefe9ef5f60438a7469da345606852f75bd60cdd6a2";
$con = pg_connect($conn_string);
if(!$con){
	echo 'Not connected to database';
	exit;
} else {
//$message = $_POST['message'];
//$title = $_POST['title'];
$message = 'New event';
$title = 'Ise';
$path = 'https://fcm.googleapis.com/fcm/send';
$server_key = 'AAAAD2RIOAo:APA91bH8PkgYDO2I2Q5H7lzP_cSxmQSBbuO-2qKJTI6je4AvwGZfVRbNg3BzEZRvjLxQMXY0BxJhJmM_Rf2L3WeW98QRkfkW7kj-KJq9UVAy0qQIVb2EAP8bC_boKgcC-LPRUh66Q_S3Csari5O4nDH9cZZAz2BLgA';
$sql = 'SELECT * FROM Token';
$result = pg_query($con, $sql);
if(!$result){
	echo "Query error.";
	exit;
} else {
if(pg_num_rows($result) > 0){
	
	while ($row = pg_fetch_row($result)){
	
		$key = $row[0];
		$headers = array('Authorization:key=' .$server_key, 'Content-Type:application/json');
		$fields = array('to'=>$key, 'notification'=>array('title'=>$title,'body'=>$message));
		$payload = json_encode($fields);
		$curl_session = curl_init();
		curl_setopt($curl_session, CURLOPT_URL, $path);
		curl_setopt($curl_session, CURLOPT_POST, true);
		curl_setopt($curl_session, CURLOPT_HTTPHEADER, $headers);
		curl_setopt($curl_session, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl_session, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($curl_session, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
		curl_setopt($curl_session, CURLOPT_POSTFIELDS, $payload);

		$resultcurl = curl_exec($curl_session);
		echo $resultcurl;
		curl_close($curl_session);
	}
}
}
}
pg_close($con);

?>