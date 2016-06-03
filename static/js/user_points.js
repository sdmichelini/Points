$(document).ready(function(){
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
var USERS_URL = '';
var USERS = [];

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
		term: $('#term').val(),
		points_completed: $('#pointsFor').val(),
		points_missed: $('#pointsAgainst').val(),
		mandatory: $('#mandatory').is(':checked'),
		user_items: []
	};
	for(var i = 0; i < USERS.length; i++){
		if($('#'+genId(USERS[i], '3')).is(':checked')){
			entry.user_items.push({user: USERS[i].email, weight: 0.0});
			alert(genId(USERS[i], '3') +":"+$('#'+genId(USERS[i],'3')).is(':checked'));
		}else if($('#'+genId(USERS[i], '1')).is(':checked')){
			if($('#weighted').is(':checked')){
				entry.user_items.push({user: USERS[i].email, weight: Number($('#'+genId(USERS[i],'4')).val())/Number($('#pointsFor').val())});
			}else{
				entry.user_items.push({user: USERS[i].email, weight: 1.0});
			}
		}else if($('#'+genId(USERS[i], '2')).is(':checked')){
			if($('#weighted').is(':checked')){
				entry.user_items.push({user: USERS[i].email, weight: Number($('#'+genId(USERS[i],'4')).val())/Number($('#pointsAgainst').val())});

			}else{
				entry.user_items.push({user: USERS[i].email, weight: 1.0});
			}
		}	
	}
	alert(JSON.stringify(entry));
}

function loadUsers(){
	var users = [
	{name: 'Test User', email: 'test@example.com'},
	{name: 'Bob' , email: 'bob@example.com'}
		];
	didFinishLoad(users);
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