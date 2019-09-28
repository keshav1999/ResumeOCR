
function edit(id){ 
  $.ajax({
	method: "POST",
	url: "Uploaddfiles.php",
	data: { id:  id, mode: 'editdetails', },
  }).done(function( data ) {
	$('#id').val(data[0]['_id']);
  });
}  