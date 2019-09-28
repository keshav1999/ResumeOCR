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
	<link rel="stylesheet" type="text/css" href="css/DataTables/dataTables.bootstrap.css"/>
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.css">
	<script src="js/jquery-3.1.1.min.js"></script>
	<script src="js/custom.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="css/DataTables/dataTables.bootstrap.js"></script>
	<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.js"></script>

<style>
th {
	background-color: #3e4444;
	color:white;
}
td{
	
}


</style>	
	
</head>

<?php

/*$conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");
$filter = [];
$options =  [
   'sort' => ['lastmodified' => -1],
];
$query = new MongoDB\Driver\Query($filter, $options);
$rows = $conn->executeQuery('Resumedb.Info', $query);
//foreach($rows as $r){ echo '<pre>';
//   print_r($r);
//} */

$m = new MongoClient();
$db = $m->Resumedb;
$collection = $db->Info;
$cursor = $collection->find()->sort(array('_id' => -1));
?>

<body>

     <nav class="navbar navbar-default sticky-top" style="width:100%; background:rgb(0,0,143); padding: 0px;">
			  <a href="index.php"><img src="images/logo.png" height="90em" style="padding-left:15%;"/></a>
			  <ul class="navbar-nav mr-auto" style="padding-left:4%;">
			    <li class="nav-item"><a style="color:white;" class="nav-link" href="index.php">Home</a></li></ul> 
				<!--<h3 style="color:white;margin-right:43%;">Candidate Details</h3>-->
			  <h2 style="color:white; padding-right:3%;">Talent Acquisition</h2>
	 </nav>

	
	
	<div class="container">
	 
	    <br> <h3>Candidate Details</h3><br>
	
								<?php if(!empty($_REQUEST['oyche'])){ ?>
	                            <div class="alert alert-info alert-dismissible" role="alert">
								  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span>
								  </button>
	                        	<?php 
	                        	
	                        		if(trim($_REQUEST['oyche'])=='ho'){ echo "Details Updated Successfully.";} 
	                        		if(trim($_REQUEST['oyche'])=='err') {echo $_REQUEST['oyche'];}
									if(trim($_REQUEST['oyche'])=='leete') {echo "Deleted Successfully";}
	                        	?>
                        		</div>
                            	<?php } ?>
		
		<!--<input id="myInput" type="text" placeholder="Search.." class="float-right" style="width:25%">
		<br><br>-->

		<table id="viewdata" class="table table-bordered nowrap" style="overflow-x: auto;"> <!----> 
		  <thead>
		  <tr>
			<th width ="10%">Name</th>
			<th width ="10%">Phone</th>
			<th width ="10%">Email</th>
			<th width ="10%">Experience</th>
			<th width ="30%">Degree</th>
			<th width ="10%">Education</th>
			<th width ="10%">Comments</th>
			<th width ="10%">Last Modified</th>
			<th width ="10%">Actions</th>
		  </tr>
		  </thead>
		  <tbody>
			  <?php $i =1; 
				 foreach ($cursor as $document) {   ?>
				  <tr>
				    <td><?php echo $document["Name"];?></td>
					<td><?php echo $document["Phone"];?></td>
					<td><?php echo $document["Email"];?></td>
					<td><?php echo $document["Experience"];?></td>
					<td><?php echo $document["Degree"];?></td>
					<td><?php echo $document["Education"];?></td>
					<td><?php echo $document["comments"];?></td>
					<td><?php echo $document["lastmodified"];?></td>
					<td><a href="editresume.php?flag=1&id=<?php echo $document["_id"]; ?>">Edit</a> |
						<a href="Uploadfiles.php?mode=del&id=<?php echo $document["_id"]; ?>&file=<?php echo $document["docpath"];?>&docid=<?php echo $document["docid"];?>" onclick="return confirm('Do you want to delete <?php echo $document['Name'];  ?>?')">Delete</td>
				  </tr>
			  <?php $i++;  } ?>
		  </tbody>
		</table>
	 
	  
	</div>

</body>

<script>
/*$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});*/

$(document).ready( function () {
    $('#viewdata').DataTable();
	} );

  $('#viewdata').DataTable( {
   // paging: false,
   // scrollY: 390,
	"ordering": false,
	"scrollX": true,
	
	"columnDefs": [
            {
                "targets": [ 4 ],
                "visible": false
            }, {
                "targets": [ 5 ],
                "visible": false
            }]
    } );


</script>


</html>