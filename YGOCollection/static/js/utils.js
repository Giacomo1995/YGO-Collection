function showdetails(rowid) {
	$('#' + rowid).toggle();
}

function selectall() {
	var items = document.getElementsByClassName('checkbox');
	for (i = 0; i < items.length; i++) {
		items[i].checked = document.getElementsByName('checkall')[0].checked
	}
}

function showpopup() {
	if (document.getElementById('addcards')) {
		setTimeout(function() {
			document.getElementById('addcardspopup').style.visibility = "visible";
			document.getElementById('addcards').style.visibility = "visible";
		}, 100);

		setTimeout(function() {
			$('#addcardspopup').hide('slow');
			$('#addcards').hide('slow');
		}, 3000);
	}
}

function addcardvalidator() {
	var items = document.getElementsByClassName('checkbox');
	for (i = 0; i < items.length; i++) {
		if (items[i].checked) {
			return true;
		}
	}

	event.preventDefault();
	alert('No cards selected.');
	return false;
}
