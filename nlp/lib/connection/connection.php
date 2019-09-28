<?php
$link = @mysqli_connect(DB_HOST, DB_USER, DB_PWD) or die('Could not connect: ' . mysql_error());//var_dump($link);
$db_selected = @mysqli_select_db(DB_NAME, $link) or die('Can\'t use DB : ' . mysql_error());//var_dump($db_selected);


/*
$rs = mysql_query("select * from region") or die(mysql_error());
$row = mysql_fetch_assoc($rs);
print_r($row);*/
?>