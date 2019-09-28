<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>AXAXL HR Bay</title>
	
	<link rel="stylesheet" type="text/css" href="css/style.css" />
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css" />
	<link rel="stylesheet" type="text/css" href="css/bootstrap-grid.css" />
	<link rel="stylesheet" type="text/css" href="css/bootstrap-reboot.css" />
	<script src="js/bootstrap.js"></script>
</head>

<body> 
<?php //$flag = urldecode($_REQUEST["flag"]); 
 $flag = isset($_REQUEST["flag"])? trim($_REQUEST["flag"]): "";

 //when trying to insert
if($flag=="jshu830dh") {

		//echo '<pre>';
	//$file = echo $_FILES['file'];
	$m = new MongoClient();
	$gridfs = $m->selectDB('Resumedb')->getGridFS();
	$docid = $gridfs->storeUpload('file', array('username' => $_POST['flag'])); 
	//echo '<pre>';  print_r($docid);  exit;

	/*******upload file******************/
	$target_dir = "resumes/";
	$new_filename = time()."_". basename($_FILES["file"]["name"]);
	$target_file = $target_dir . $new_filename; 
	$FileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
    $pythonScript = 'scripts/nlp1-UI.py';
	$pythonExec = 'C:\Users\X122866\AppData\Local\Continuum\Anaconda3\python.exe';
	//$tmppath="C:\XL_Apps\wamp\www\\nlp\\resumes\\";
	$tmppath="C:\XL_Apps\\Xampp\htdocs\\nlp\\resumes\\";
	$path= $tmppath.$new_filename;
    //$path= $_FILES["file"]["tmp_name"];
	// Check if file already exists
	if (file_exists($target_file)) {
		header("Location: index.php?ooyee=dhuhed"); exit;
	}
	// Allow certain file formats
	if($FileType != "docx" && $FileType != "pdf" && $FileType != "doc" ) {
		header("Location: index.php?ooyee=gduidg"); exit;
	}

	if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) { 
		//echo "The file ". basename( $_FILES["file"]["name"]). " has been uploaded.";
	} else {
		echo "Sorry, there was an error uploading your file.";
		exit;
	}


	/**********************call python script**********************/
	  clearstatcache();
	  if (!file_exists($pythonExec)) { exit("The python executable '$pythonExec' does not exist!"); }
	  if (!is_executable($pythonExec)) { exit(("The python executable '$pythonExec' is not executable!"));}
	  if (!file_exists($pythonScript)) {exit("The python script file '$pythonScript' does not exist!");} 

	 exec("$pythonExec $pythonScript \"$path\" \"$FileType\" ", $outputq, $return); 
	 //echo "$pythonExec $pythonScript \"$path\" \"$FileType\" "; exit;

	/**********************move to editresume**********************/
	  
	  if($return != 0) { header("Location: index.php?ooyee=uittug"); exit;}
	  else {
		  $output=array();
		  foreach($outputq as $value)
			{
				if($value=="Warning: parsing empty text") {continue;}
				else{ $output[]=$value; }     
			} 
			//echo '<pre>'; 
			//print_r($output); exit;   
			     
	  $name=$output[0]; $phone=$output[1]; $email=$output[2]; 
	  //$name=""; $phone=""; $email=""; 
	  $Experience=$output[3]; $Degree=$output[4] ;  $Education=$output[5];
	  $resume = $target_file; $type = $FileType; $comments="";  
	}


}
 
 
//when trying to edit 		
else { //$name=urldecode($_GET["name"]); $phone=urldecode($_GET["phone"]); $email=urldecode($_GET["email"]); $comments=urldecode($_GET["comments"]);
	  
	    $id    = urldecode($_REQUEST["id"]);
		/*$conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
		$filter = ['_id' => new MongoDB\BSON\ObjectID($id)];
		$options =  [];
		$query = new MongoDB\Driver\Query($filter, $options);
		$rows = $conn->executeQuery('Resumedb.Info', $query);
		foreach($rows as $row){
			$type= $row->doctype;
			$resume= $row->docpath;
			$name= $row->Name;
			$phone= $row->Phone;
			$email= $row->Email;
			$Experience= $row->Experience;
			$Degree= $row->Degree;
			$Education= $row->Education;
			$comments= $row->comments;
		}*/
		$m = new MongoClient();
	    $db = $m->Resumedb;
		$result = $db->Info->findOne(array('_id' => new MongoId($id)));
		    $type= $result['doctype'];
			$resume= $result['docpath'];
			$name= $result['Name'];
			$phone= $result['Phone'];
			$email= $result['Email'];
			$Experience= $result['Experience'];
			$Degree= $result['Degree'];
			$Education= $result['Education'];
			$comments= $result['comments'];
			$docid= $result['docid'];
	  }
?>

     <nav class="navbar navbar-default sticky-top" style="width:100%; background:rgb(0,0,143); padding: 0px;">
			  <a href="index.php"><img src="images/logo.png" height="100em"/ style="padding-left:15%;"></a>
			  <h2 style="color:white;padding-right:3%;">Talent Acquisition</h2>
	 </nav>
	 
	<div class="container">
     <div class="row">
	 
	  <?php if($type=="pdf") { ?>
	  <div class="col-xs-6">
	  <embed src="savefiletomongo.php?docid=<?php echo $docid ; ?>" width="800px" height="655px" style="overflow:scroll;"/>
	  </div>
	  <?php }?>
	  
	  <div class="col-xs-6" style="padding-left:1%; padding-bottom:2%; width:47.2%;height:655px;overflow:scroll;overflow-x: hidden; scrollbar-width: none;">
	  <div class="container">
	  <br><h2>Update Details</h2><br>
			  <form action="uploadfiles.php" style="width: 100% !important;">
			    <input type="hidden" name="mode" value="savetomongo" />
				<input type="hidden" name="flag" value="<?php echo $flag; ?>" />
				<input type="hidden" name="filepath" value="<?php echo $resume; ?>" />
				<input type="hidden" name="filetype" value="<?php echo $type; ?>" />
				<input type="hidden" name="docid" value="<?php echo $docid; ?>" />
				<?php if($flag==1) { ?> <input type="hidden" name="id" value="<?php echo $id; ?>" /> <?php } ?>
				<div class="form-group">
				  <label for="Name">Name:</label>
				  <input type="text" class="form-control" id="Name" placeholder="" name="Name" value="<?php echo str_replace(array("['","']"),"",$name);?>" autocomplete="off">
				</div>
				<div class="form-group">
				  <label for="pwd">Phone:</label>
				  <input type="text" class="form-control" id="Phone" placeholder="" name="Phone" value="<?php echo str_replace(array("['","']"),"",$phone);?>" autocomplete="off">
				</div>
				<div class="form-group">
				  <label for="email">Email:</label>
				  <input type="text" class="form-control" id="Email" placeholder="" name="Email" value="<?php echo str_replace(array("['","']"),"",$email);?>" autocomplete="off">
				</div>
				<div class="form-group">
					<label for="comments">Experience:</label>
					<textarea class="form-control" id="Experience" name="Experience" rows="3" autocomplete="off"><?php echo str_replace(array("['","']"),"",$Experience);?></textarea>
				</div>
				<div class="form-group">
					<label for="comments">Degree:</label>
					<textarea class="form-control" id="Degree" name="Degree" rows="3" autocomplete="off"><?php echo $Degree;?></textarea>
				</div>
				<div class="form-group">
					<label for="comments">Education:</label>
					<textarea class="form-control" id="Education" name="Education" rows="3" autocomplete="off"><?php echo str_replace(array("['","']"),"",$Education);?></textarea>
				</div>
				<div class="form-group">
					<label for="comments">Comments</label>
					<textarea class="form-control" id="comments" name="comments" rows="3" autocomplete="off"><?php echo str_replace(array("['","']"),"",$comments);?></textarea>
				</div>
				<?php if($type!=="pdf") { ?> <a href="<?php echo $resume ; ?>">Download Resume</a><br><br><?php }?>
				<button type="submit" class="btn btn-info float-right">Save</button>
			  </form>
		</div>
	  </div>
	  
	  
	
	  
     </div>
	</div>

</body>



</html>