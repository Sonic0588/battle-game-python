
function ask(ev){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			if (JSON.parse(xhr.responseText)['result']['response'] === true){
				//var room_number = JSON.parse(xhr.responseText)['result']['room_number'];
				window.location.replace('/game');
			}
		}
	}
	xhr.open('GET', '/ask', true);
	xhr.send();
}

function main(){
	setInterval(ask, 1000)
}


document.addEventListener('DOMContentLoaded', main)