
<?php
$docid= $_REQUEST['docid'];
$m = new MongoClient();
$gridfs = $m->selectDB('Resumedb')->getGridFS();
$image = $gridfs->findOne(array('_id' => new MongoId($docid)));
$pdf= $image->getBytes(); 
header("Content-type: application/pdf");
echo $pdf;
?>