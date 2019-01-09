function waiting_for_other_player(){
	console.log('Start waiting');
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/step/waiting', true);
	xhr.send();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			var result = JSON.parse(xhr.responseText)['result'];
			console.log(result);
			if (result != 'waiting'){
				if (result == 'finish'){
					alert('Выиграл ' + JSON.parse(xhr.responseText)['winner'] + ' !');
				}
				else{
					var hp_p1 = document.querySelector('.player_1_hp');
					hp_p1.innerHTML = result['player_1']['hp'];
					var hp_p2 = document.querySelector('.player_2_hp');
					hp_p2.innerHTML = result['player_2']['hp'];
					fight();
				}
			}
			else{
				waiting_for_other_player()
			}
		}
	}
}

function send_step(){
	if ('attack' in step && 'defence' in step){
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/step', true);
		xhr.send(JSON.stringify(step));
		xhr.onreadystatechange = function(){
			if (xhr.readyState == 4){
				var result = JSON.parse(xhr.responseText)['result'];
				if (result){
					waiting_for_other_player();
				}
			}
		}
		step = {}
	} else{
		alert('Не выбрано защита или атака!')
	}
}

function defence(ev){
	var el = ev.target;
	var parts = document.querySelectorAll('.body_defence');
	[].forEach.call(parts, function(item){
		item.classList.remove('gamer-body__item_active');
	});
	el.classList.toggle('gamer-body__item_active');
	if (el.id =='def_head'){
		step['defence'] = 'head';
	} else if (el.id =='def_body'){
		step['defence'] = 'body';
	} else if (el.id =='def_legs'){
		step['defence'] = 'legs';
	}
}


function attack(ev){
	var el = ev.target;
	var parts = document.querySelectorAll('.body_attack');
	[].forEach.call(parts, function(item){
		item.classList.remove('gamer-body__item_active');
	});
	el.classList.toggle('gamer-body__item_active');
	if (el.id =='atk_head'){
		step['attack'] = 'head';
	} else if (el.id =='atk_body'){
		step['attack'] = 'body';
	} else if (el.id =='atk_legs'){
		step['attack'] = 'legs';
	}
}


function fight(){
	var hp_p1 = parseFloat(document.querySelector('.player_1_hp').innerHTML);
	var hp_p2 = parseFloat(document.querySelector('.player_2_hp').innerHTML);
	var atk = document.querySelector('#attack');
	atk.addEventListener('click', attack);
		// console.log(step);
	var def = document.querySelector('#defence');
	def.addEventListener('click', defence);
	var btn = document.querySelector('.game__btn');
	btn.addEventListener('click', send_step);

}

function parse_stat(player, result){
	var player_name = document.querySelector('.' + player + '_name');
	player_name.innerHTML = result[player]['name'];
	var hp = document.querySelector('.' + player + '_hp');
	hp.innerHTML = result[player]['hp'];
	var damage = document.querySelector('.' + player + '_damage');
	damage.innerHTML = result[player]['damage'];
	var evasion = document.querySelector('.' + player + '_evasion');
	evasion.innerHTML = result[player]['evasion'];
	var maxhp = document.querySelector('.' + player + '_maxhp');
	maxhp.innerHTML = result[player]['hp'];
}

function ask_stat(path){
	if (path == '/game/first_ask'){
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function(){
			if (xhr.readyState == 4){
				var result = JSON.parse(xhr.responseText)['result']
				parse_stat('player_1', result);
				parse_stat('player_2', result);
				fight();
			}
		}
		xhr.open('GET', path, true);
		xhr.send();
	}
}

function main(){
	ask_stat('/game/first_ask');
	
}

var step = {};

document.addEventListener('DOMContentLoaded', main);