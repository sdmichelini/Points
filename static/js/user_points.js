$(document).ready(function(){
	loadParams();
	if(PARAMS['config'] == '1'){
		$('#weighted').prop('checked', true);
	}else if(PARAMS['config'] == '2'){
		$('#mandatory').prop('checked', true);
	}
	loadUsers();
	$('#weighted').change(function(){
		setWeightDisabled(!$('#weighted').is(':checked'));
	});
	$('#pointsSubmit').on('submit', function(e){
		e.preventDefault();
		submitPoints();
	});
});

//TODO: Add Users URL
var USERS_URL = '/admin/points';
var USERS = [];
var PARAMS = [];

function loadParams(){
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for(var i = 0; i < hashes.length; i++)
	{
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	PARAMS = vars;
}

function submitPoints(){
	//Validiate form
	if($('#eventTitle').val() == ''){
		alert('Please Fill Out Event Title.');
		return;
	}else if($('#eventDescription').val() == ''){
		alert('Please Fill Out Event Description.');
		return;
	}else if($('#pointsFor').val() == ''){
		alert('Please Fill Out Points For Completion');
		return;
	}else if($('#pointsAgainst').val() ==''){
		alert('Please Fill Out Points For Failure.');
		return;
	}
	var entry = {title: $('#eventTitle').val(),
		description: $('#eventDescription').val(),
		term: $('#termSelect').val(),
		points_completed: $('#pointsFor').val(),
		points_missed: $('#pointsAgainst').val(),
		mandatory: $('#mandatory').is(':checked'),
		user_items: []
	};
	for(var i = 0; i < USERS.length; i++){
		if($('#'+genId(USERS[i], '3')).is(':checked')){
			entry.user_items.push({user: USERS[i].email, weight: 0.0, completed: true});
			alert(genId(USERS[i], '3') +":"+$('#'+genId(USERS[i],'3')).is(':checked'));
		}else if($('#'+genId(USERS[i], '1')).is(':checked')){
			if($('#weighted').is(':checked')){
				entry.user_items.push({user: USERS[i].email, weight: Number($('#'+genId(USERS[i],'4')).val())/Number($('#pointsFor').val()), completed: true});
			}else{
				entry.user_items.push({user: USERS[i].email, weight: 1.0, completed: true});
			}
		}else if($('#'+genId(USERS[i], '2')).is(':checked')){
			if($('#weighted').is(':checked')){
				entry.user_items.push({user: USERS[i].email, weight: Number($('#'+genId(USERS[i],'4')).val())/Number($('#pointsAgainst').val()), completed: false});

			}else{
				entry.user_items.push({user: USERS[i].email, weight: 1.0, completed: false});
			}
		}
	}
	alert(JSON.stringify(entry));
	$.ajax({
		type: 'POST',
		url: USERS_URL,
		data: JSON.stringify(entry),
		success: function(msg){
			console.log('Success');
			location.reload();
		},
		error: function(){
			alert('Error Submitting Form');
		 }
	});
}

function loadUsers(){

	$.get('/users',function(data){
		var users = [];
		for(var email in data.result) {
			users.push({name:data.result[email], email: email });
		}
		didFinishLoad(users);
	});
	/*
	var users = [
	{name: 'Test User', email: 'test@example.com'},
	{name: 'Bob' , email: 'bob@example.com'}
];*/

}

function didFinishLoad(users){
	html = '<h3>Users</h3><br>';
	for(var i = 0; i < users.length; i++){
		html += createUserHtml(users[i]);
	}
	USERS = users;
	$('#userEntry').html(html);
	setWeightDisabled(true);
}

function createUserHtml(user){
	return "<li class='list-group-item' style='height: 4em;'>"+user.name+
		"<div class='btn-group pull-xs-right' data-toggle='buttons'>"+
			"<label class='btn btn-success-outline'>"+
				"<input type='radio' id='"+user.email.replace("@","").replace(".","")+'1'+"' autocomplete='off'>P"+
			"</label>"+
			"<label class='btn btn-primary-outline'>"+
				"<input type='radio' id='"+user.email.replace("@","").replace(".","")+'2'+"' autocomplete='off'>A"+
			"</label>"+
			"<label class='btn btn-danger-outline'>"+
				"<input type='radio' id='"+user.email.replace("@","").replace(".","")+'3'+"' autocomplete='off'>E"+
			"</label>"+
			"<fieldset id='"+user.email.replace("@","").replace(".","")+'5'+"'><input type='number' id='"+user.email.replace("@","").replace(".","")+'4'+"'></fieldset>"+
			"</div></li>";

}

function genId(user, number){
	return user.email.replace("@","").replace(".","")+number;
}

function setWeightDisabled(disable){
	console.log(USERS);
	if(disable == true){
		for(var i = 0; i < USERS.length; i++){
			$('#'+genId(USERS[i],'5')).prop('disabled', true);
		}
	}else if(disable == false){
		for(var i = 0; i < USERS.length; i++){
		$('#'+genId(USERS[i],'5')).prop('disabled', false);
		}
	}
}
