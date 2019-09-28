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


    <div id="background"></div>
    <div id="midground"></div>
    <div id="foreground"></div>
	
	<div id="page-wrap" style="position: relative; width:450px;"> 
    <br><br><br><br><br><br><br>
	
	
		
	<div id="" class="circle">	
	  <center><a href="index.php"><img src="images/logo2.png" width="42%;"/></a></center>
		<center><h2 style="color:white;">Talent Acquisition</h2></center>
		<hr>
		<?php if(!empty($_REQUEST['ooyee'])){ ?>
	                            <div class="alert alert-info alert-dismissible" role="alert">
								  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span>
								  </button>
	                        	<?php 
	                        		if(trim($_REQUEST['ooyee'])=='dhuhed'){echo "Sorry, file already exists. Please change the file name and try again. ";} 
	                        		if(trim($_REQUEST['ooyee'])=='gduidg') {echo "Sorry, only pdf & word documents are accepted.";}
									if(trim($_REQUEST['ooyee'])=='uittug') {echo "Error in Python script";}
	                        	?>
                        		</div>
															<?php } ?>
		
		
		
		<center>
	  <form action="editresume.php" enctype="multipart/form-data" method="post" class="" id="uploadForm">
	                    <input type="hidden" name="flag" value="jshu830dh" />
						<input type="file" id='file' name="file" style="border: 1px solid #ddd; padding: 10px;"/><br>	
						<input type="submit" value="Upload Resumes" name="Upload" class="button button2 abcbutton"/><br>
       
								
								
		</form>
		<a href="details.php"><button class="button button2">Candidate Details</button></a> <br><br>
								</center>   <p id="demo"></p>                     
	</div>
	
    <img src="images/loader.gif" style="margin-left:40%; margin-top:5%; visibility:hidden;" class="gif">

	 </div>

</body>

<script>

$('#uploadForm').submit(function() {
    $('.gif').css('visibility', 'visible');
});

</script>



</html>