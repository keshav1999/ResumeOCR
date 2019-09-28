<?php

$mode = isset($_REQUEST["mode"])? trim($_REQUEST["mode"]): "";
switch ($mode) {

	case "savetomongo":
		    savetomongo();
		    break;
	case "del":
		    deleterecords();
		    break;
}


function savetomongo(){
	
	$Name = $_REQUEST['Name']; $Phone = $_REQUEST['Phone']; $Email = $_REQUEST['Email']; $Experience = $_REQUEST['Experience']; $Degree = $_REQUEST['Degree'];
	$Education = $_REQUEST['Education']; $comments = $_REQUEST['comments']; $filepath = $_REQUEST['filepath']; $docid = $_REQUEST['docid'];
	$filetype = $_REQUEST['filetype']; $flag = $_REQUEST['flag']; if($flag==1) { $id = $_REQUEST['id']; }
   
try{
	//$conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
	//$inserts = new MongoDB\Driver\BulkWrite();
	$m = new MongoClient();
	$db = $m->Resumedb;
	$collection = $db->Info;
  
	//insert
	if($flag=="jshu830dh") {
	$document = array(
		'Name' => $Name,
		'Phone' => $Phone,
		'Email' => $Email,
		'Experience' => $Experience,
		'Degree' => $Degree,
		'Education' => $Education,
		'comments' => $comments,
		'lastmodified' => date('F d Y') ,
		'docpath' => $filepath,
		'doctype' => $filetype,
		'docid' => $docid
	);
	//$inserts->insert($user1);
	//$conn->executeBulkWrite("Resumedb.Info", $inserts);*/
	 
	$collection->insert($document);

	}
	
	//update
	if($flag==1) {
		
		/*$inserts->update(
		  ['_id'=>new MongoDB\BSON\ObjectID($id)],
		  ['$set' => [  'Name' => $Name,
						'Phone' => $Phone,
						'Email' => $Email,
						'Experience' => $Experience,
						'Degree' => $Degree,
						'Education' => $Education,
						'comments' => $comments,
						'lastmodified' => date('F d Y') ,
						'docpath' => $filepath,
						'doctype' => $filetype]], 
		  ['multi' => false, 'upsert' => false]
		  );
				  
		$writeConcern = new MongoDB\Driver\WriteConcern(MongoDB\Driver\WriteConcern::MAJORITY, 1000);
				 
		 $result       = $conn->executeBulkWrite('Resumedb.Info', $inserts, $writeConcern);*/
		 
		$criteria = array("_id"=>new MongoId($id));
        $newdata = array('$set'=>array( "Name"=>$Name,
		"Phone" => $Phone,
		"Email" => $Email,
		"Experience" => $Experience,
		"Degree" => $Degree,
		"Education" => $Education,
		"comments" => $comments,
		"lastmodified" => date('F d Y') ,
		"docpath" => $filepath,
		"doctype" => $filetype));

		$ret = $collection->update( $criteria, $newdata);
        var_dump($ret);

	}
	
	header("Location: details.php?oyche=ho");
	exit;
 }
 
	catch (MongoDB\Driver\Exception\AuthenticationException $e) {

		echo "Exception:", $e->getMessage(), "\n";
	} catch (MongoDB\Driver\Exception\ConnectionException $e) {

		echo "Exception:", $e->getMessage(), "\n";
	} catch (MongoDB\Driver\Exception\ConnectionTimeoutException $e) {

		echo "Exception:", $e->getMessage(), "\n";
	}
	
}

function deleterecords(){
	$id= $_GET['id'];  $path= $_GET['file'];  $docid= $_GET['docid'];
	//$conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
	
	if($id){

		$m = new MongoClient();
		$db = $m->Resumedb;
		$collection = $db->Info;
		$collection->remove(array('_id'=> new MongoId($id)));
	
		$gridfs = $m->selectDB('Resumedb')->getGridFS();
		$gridfs->remove(array('_id'=> new MongoId($docid)));

		unlink($path);
    /*  $delRec = new MongoDB\Driver\BulkWrite;
		$delRec->delete(['_id' =>new MongoDB\BSON\ObjectID($id)], ['limit' => 1]);
		$writeConcern = new MongoDB\Driver\WriteConcern(MongoDB\Driver\WriteConcern::MAJORITY, 1000);
		$result       = $conn->executeBulkWrite('Resumedb.Info', $delRec, $writeConcern);
	*/
	

	header("Location: details.php?oyche=leete");
        exit;
	}    
}	

?>