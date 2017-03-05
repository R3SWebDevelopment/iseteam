<?php
$conn_string = "host=ec2-54-225-127-147.compute-1.amazonaws.com port=5432 dbname=d8vkt7mt6uqvqh user=fyjwzhtytojrxi password=c100d9cde99b45d5e4f2acefe9ef5f60438a7469da345606852f75bd60cdd6a2";
$con = pg_connect($conn_string);
if(!$con){
	echo 'Not connected to database';
	exit;
} else{
$response = array();
 
// connecting to db
$sql = "SELECT * FROM Ambassador ORDER BY name";
$result = pg_query($con, $sql);
if(!$result){
	echo 'Query error';
	exit;
} else{

if (pg_num_rows($result) > 0) {
    // looping through all results
    // ambassador node
    $response["ambassador"] = array();
 
	while ($row = pg_fetch_row($result)) {
		// temp user array
        $ambassador = array();
        $ambassador["id"] = $row[0];
        $ambassador["name"] = $row[1];
 
        // push single new into final response array
        array_push($response["ambassador"], $ambassador);
	}
	$response["success"] = 1;
	echo json_encode($response);
} else {
    // no staff found
	$response["success"] = 0;
    $response["message"] = "No ambassador found";
 
    // echo no users JSON
    echo json_encode($response);
}
}
}
pg_close($con);
?>