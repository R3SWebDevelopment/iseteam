<?php
$conn_string = "host=ec2-54-225-127-147.compute-1.amazonaws.com port=5432 dbname=d8vkt7mt6uqvqh user=fyjwzhtytojrxi password=c100d9cde99b45d5e4f2acefe9ef5f60438a7469da345606852f75bd60cdd6a2";
$con = pg_connect($conn_string);
if(!$con){
	echo 'Not connected to database';
	exit;
} else {
$response = array();
 
// connecting to db
$dtString = date("Y/m/d");
$sql = "SELECT * FROM Event WHERE (date >= '$dtString') ORDER BY date DESC";
$result = pg_query($con, $sql);
if(!$result){
	echo 'Query error';
} else{
if (pg_num_rows($result) > 0) {
    // looping through all results
    // event node
    $response["event"] = array();
 
    while ($row = pg_fetch_row($result)) {
        // temp user array
        $event = array();
        $event["id"] = $row[0];
        $event["title"] = $row[1];
		$event["description"] = $row[2];
		$event["date"] = $row[3];
		$event["cost"] = $row[4];
		$event["image"] = $row[5];
 
        // push single new into final response array
        array_push($response["event"], $event);
    }
	$response["success"] = 1;
	echo json_encode($response);
} else {
    // no events found
	$response["success"] = 0;
    $response["message"] = "No events found";
 
    // echo no users JSON
    echo json_encode($response);
}
}
}
pg_close($con);
?>