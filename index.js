
function send_info(){
	var name = document.querySelector('#reg-name');
	var strenght = document.querySelector('#reg-power');
	var agility = document.querySelector('#reg-agility');
	var endurance = document.querySelector('#reg-endurance');
	var body = {
			'name':name.value,
			'strenght':strenght.value,
			'agility':agility.value,
			'endurance':endurance.value};
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			response = JSON.parse(xhr.responseText)['result'];
			if (response == 'char_success'){
				window.location.replace('/lobby');
			}
		}
	}
	xhr.open('POST', '/character/create', true);
	xhr.send(JSON.stringify(body));
}

function validation(ev, element){
	console.log('Валидация сработала')
	var re = /^[1-8]{1}$/;
	var valid = re.test(element.value);
	if(valid){
		element.classList.add('valid_form')
	}
	else{
		element.classList.add('no_valid_form')
	}
}

function calc_stats_sum(strenght, agility, endurance){
	str = parseInt(strenght.value);
	agil = parseInt(agility.value);
	endur = parseInt(endurance.value);
	sum = str + agil + endur;
	console.log(sum);
	if(sum == 10){
		return true
	}
	else{
		return false
	}
}

function main(){
	var strenght = document.querySelector('#reg-power');
	strenght.onchange = function(ev){ //bind
		console.log('Колбек сработал')
		validation(ev, strenght);
	}
	var agility = document.querySelector('#reg-agility');
	agility.onchange = function(ev){ //bind
		validation(ev, agility);
	}
	var endurance = document.querySelector('#reg-endurance');
	endurance.onchange = function(ev){ //bind
		validation(ev, endurance);
	}

	// var strenght = document.querySelector('#reg-power');
	// strenght.addEventListener('input', function(){
	// 	
	// 	if (valid){
	// 		console.log('Заебок');
	// 	}
	// 	else {
	// 		console.log('Ввел хуйню!');
	// 	}
	// });
	// var name = document.querySelector('#reg-name');
	// var agility = document.querySelector('#reg-agility');
	// var endurance = document.querySelector('#reg-endurance');
	// var fields = document.querySelectorAll('.field');
	var el = document.querySelector('#js-button')
	el.onclick = function(ev){ // определить в колбеке элементы еще раз, тк они будут не видны
		if(calc_stats_sum(strenght, agility, endurance)){
			send_info()
		}
		else{
			alert('Сумма параметров персожана должна равняться 10 пунктам')
		}
	}
}


document.addEventListener('DOMContentLoaded', main)