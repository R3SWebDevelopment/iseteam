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
$dt = date_create($dtString);
$prev_dt = date_sub($dt, date_interval_create_from_date_string('1 month'));
$old_dt = date_format($prev_dt, 'Y/m/d');
$sql = "SELECT * FROM New WHERE (date BETWEEN '$old_dt' AND '$dtString') ORDER BY date DESC";
$result = pg_query($con, $sql);
if(!$result){
	echo 'Query error';
	exit;
} else {
if (pg_num_rows($result) > 0) {
    // looping through all results
    // news node
    $response["news"] = array();
 
    while ($row = pg_fetch_row($result)) {
        // temp user array
        $news = array();
        $news["id"] = $row[0];
        $news["title"] = $row[1];
        $news["description"] = $row[2];
        $news["date"] = $row[3];
 
        // push single new into final response array
        array_push($response["news"], $news);
    }
	$response["success"] = 1;
	echo json_encode($response);
} else {
    // no news found
	$response["success"] = 0;
    $response["message"] = "No news found";
 
    // echo no users JSON
    echo json_encode($response);
}
}
}
pg_close($con);
?>