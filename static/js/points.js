$(document).ready(function(){
	loadPoints();
	loadUsers();
});

var USERS = {}
var POINTS = {}

function loadUsers(){
	$.get('/users', function(data){
		if(data.result){
			for(user in data.result){
				USERS[user.replace("@","").replace(".","")] = data.result[user];
			}
			console.log(USERS);
			console.log('Users Added');
		}
	});
	if(POINTS.length > 0)updatePoints();
}

function generatePointsLink(email){
	return '/users/'+btoa(email);
}

function updatePoints(){
	
		var items = Object.keys(POINTS).map(function(key){
			return [key, POINTS[key]];
		});
		items.sort(function(one, two){
			return two[1] - one[1];
		});
		console.log(items);
		var htmlAdd = '';
		for(var i = 0; i < items.length; i++){
			name = items[i][0];
			if(USERS[name.replace("@","").replace(".","")])name=USERS[name.replace("@","").replace(".","")];
			console.log(USERS[name.replace("@","").replace(".","")]);
			htmlAdd += '<tr><th scope="row">' + (i+1) + '</th>'+
			'<td><a href="'+generatePointsLink(items[i][0])+'">'+name+'</a></td><td>'+items[i][1]+'</td></tr>';
		}
		$('#pointsResults').html('');
		$('#pointsResults').html(htmlAdd);
}

function loadPoints(){
	$.get('/api/points',function(data){
		if(!data.result){
			$('#pointsResults').html('API Error.');
			return;
		}else if(data.result.length == 0){
			$('#pointsResults').html('No points in system');
			return;
		}
		//Sort by largest
		POINTS = data.result;
		updatePoints();
	}).fail(function(){
		$('#pointsResults').html('Unable to load latest points data.');
	});
}
