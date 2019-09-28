<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	
  <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>AXAXL HR Bay</title>
	
	<link rel="stylesheet" type="text/css" href="css/style.css" />
	
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
  <script src="//oss.maxcdn.com/jquery.form/3.50/jquery.form.min.js"></script>
  
  <style>

  </style>
  
</head>

<body>

<?php
$manager = new MongoDB\Driver\Manager('mongodb://localhost:27017');
$bucket = (new MongoDB\Client)->test->selectGridFSBucket();
//$bucket = new MongoDB\GridFS\Bucket($manager, 'Resumedb');
//$input = fopen('resumes/1559120230_MahimaSaxenaResume.pdf', 'rb');
//$bucket->uploadFromStream('example', $input, ['chunkSizeBytes' => 14680064]);
//$bucket = new MongoDB\Driver\Manager("mongodb://localhost:27017");
//$file = fopen('resumes/1559120230_MahimaSaxenaResume.pdf', 'rb');



?>


</body>
</html>