import json
import codecs
import fnmatch
import static
import uuid
import re
import random

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server



# USERS = {}
# READY = []
# MATCH = {}
# FIGHT_LOGS = {}
# COUNTER = 0

USERS = {}
READY = []
MATCH = {}
ROOMS = {}
FIGHT_LOGS = {}

def test(where):
	print(where)
	print('READY', READY)
	print('MATCH', MATCH)
	print('ROOMS', ROOMS)
	print('FIGHT_LOGS', FIGHT_LOGS)

class User: # класс пользователя в котором храниться кука, имя пользователя и готовность игрока к бою
	def __init__(self, _id):
		self.id = _id
		self.character = None
	# name
	def is_ready(self):
		return self.character is not None


class Character: # класс персонажа наследуется от пользователя. В этом классе содержатся все характеристики персонажа и его действия
	def calc_max_hp(self):
		max_hp = (self.endurance * 100) / 8
		self.hp = max_hp

	def damage(self):
		return (self.strenght * 10) / 8

	def evasion(self):
		return (self.agility * 30) / 8

	def take_damage(self, damage):
		self.hp -= damage

	def dump(self):
		return {'name': self.name,
				'hp': self.hp,
				'damage': self.damage(),
				'evasion': self.evasion()}



test_id = str(uuid.uuid4())
USERS[test_id] = User(test_id)
player = USERS[test_id]
player.character = Character()
player.character.name = "Vaska"
player.character.strenght = 1
player.character.endurance = 1
player.character.agility = 8
player.character.calc_max_hp()
READY.append(test_id)

# 	strenght
# 	endurance
# 	agility

# 	def hit(self):
# 		pass

# 	def defend(self):
# 		pass

def index(environ, start_response):
	status = '200 OK'
	if not 'HTTP_COOKIE' in environ:
		_id = str(uuid.uuid4())
		response_headers = [('Content-type','text/html'),
							('Set-Cookie', 'uuid=' + _id + '; Path=/; Domain=localhost')]
		USERS[_id] = User(_id)
	else:
		_id = environ['HTTP_COOKIE'].split('=')[1]
		if _id not in USERS:
			USERS[_id] = User(_id)
		response_headers = [('Content-type','text/html')]
		# print(USERS[environ['HTTP_COOKIE'].split('=')[1]])
	start_response(status, response_headers)
	return [static.index.encode()]

def styles(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'text/css')]
	start_response(status, response_headers)
	return [static.styles.encode()]

def javascript(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'application/javascript')]
	start_response(status, response_headers)
	return [static.js.encode()]

def index_game(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'application/javascript')]
	start_response(status, response_headers)
	return [static.index_game.encode()]

def not_found(environ, start_response):
	start_response('404 Not Found', [('Content-type','text/html')])
	return [static.not_found_var.encode()]

def character_create(environ, start_response): # принимаем аргументы от клиента для создания перса
	content_len = int(environ.get('CONTENT_LENGTH',0) or 0)
	body = json.loads(environ['wsgi.input'].read(content_len).decode('utf-8'))
	_id = environ['HTTP_COOKIE'].split('=')[1]
	player = USERS[_id]
	player.character = Character()
	player.character.name = body["name"]
	player.character.strenght = int(body['strenght'])
	player.character.endurance = int(body['endurance'])
	player.character.agility = int(body['agility'])
	player.character.calc_max_hp()
	READY.append(_id)
	response_body = [json.dumps({'result': 'char_success'}).encode()]
	start_response('200 OK', [('Content-type', 'text/plain')])
	return response_body

def lobby(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type','text/html')]
	start_response(status, response_headers)
	return [static.lobby.encode()]

def lobby_js(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'application/javascript')]
	start_response(status, response_headers)
	return [static.lobby_js.encode()]

def ask(environ, start_response):# Функция мониторит готовность второго игрока
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	if len(READY) >= 2: # Придумать механизм очереди и редиректа двух игроков в игру
		first = READY.pop(0)
		second = READY.pop(0)
		for room in range(5):
			room = str(room)
			if not room in MATCH:
				print(room)
				FIGHT_LOGS[room] = {}
				# тест с Васькой
				FIGHT_LOGS[room][test_id] = {}
				FIGHT_LOGS[room][test_id]['attack'] = 'head'
				FIGHT_LOGS[room][test_id]['defence'] = 'head'
				# конец теста
				MATCH[room] = (first, second)
				USERS[first].character.opponent_id = second
				USERS[second].character.opponent_id = first
				ROOMS[first] = room
				ROOMS[second] = room
				break
		return [json.dumps({'result':{'room_number':room, 'response':True}}).encode()]
	else:
		return [json.dumps({'result': {'response':False}}).encode()]

def game(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type','text/html')]
	start_response(status, response_headers)
	return [static.game.encode()]

def send_img(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type','image/png')]
	start_response(status, response_headers)
	return [static.image]

def first_stat_ask(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	_id = environ['HTTP_COOKIE'].split('=')[1]
	room_number = ROOMS[_id]
	player_1 = USERS[_id].character.dump()
	opponent_id = USERS[_id].character.opponent_id
	player_2 = USERS[opponent_id].character.dump()
	result = {'result':
				{'player_1': player_1,
				 'player_2': player_2}
			}
	return [json.dumps(result).encode()]

def calc_step(room, p_1_id, p_2_id):
	move = FIGHT_LOGS[room]
	player_1 = move[p_1_id]
	player_2 = move[p_2_id]
	if player_1['attack'] != player_2['defence']:
		if USERS[p_2_id].character.evasion() < random.uniform(1.0, 100.0):
			USERS[p_2_id].character.take_damage(USERS[p_1_id].character.damage())
		else:
			print('Оппонент отразил удар!')
	if player_2['attack'] != player_1['defence']:
		if USERS[p_1_id].character.evasion() < random.uniform(1.0, 100.0):
			USERS[p_1_id].character.take_damage(USERS[p_2_id].character.damage())
		else:
			print('Вы отразили удар!')
	move = {'done'}


def step(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	content_len = int(environ.get('CONTENT_LENGTH',0) or 0)
	body = json.loads(environ['wsgi.input'].read(content_len).decode('utf-8'))
	print(body)
	char_id = environ['HTTP_COOKIE'].split('=')[1]
	room = ROOMS[char_id]
	FIGHT_LOGS[room][char_id] = {}
	FIGHT_LOGS[room][char_id]['attack'] = body['attack']
	FIGHT_LOGS[room][char_id]['defence'] = body['defence']
	return [json.dumps({'result':True}).encode()]

def waiting(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	char_id = environ['HTTP_COOKIE'].split('=')[1]
	opponent_id = USERS[char_id].character.opponent_id
	room = ROOMS[char_id]
	if FIGHT_LOGS[room] == 'done':
		FIGHT_LOGS[room] = {};
		if USERS[char_id].character.hp < 0 or USERS[opponent_id].character.hp < 0:
			if USERS[char_id].character.hp > USERS[opponent_id].character.hp:
				winner = 'player_1'
			else:
				winner = 'player_2'
			return [json.dumps({'result': 'finish', 'winner': winner}).encode()]
		else:
			player_1 = USERS[char_id].character.dump()
			player_2 = USERS[opponent_id].character.dump()
			result = {'result':
							{'player_1': player_1,
							 'player_2': player_2}}
			return [json.dumps(result).encode()]
	if not char_id in FIGHT_LOGS[room]: # если еще нет хода от игрока
		FIGHT_LOGS[room][char_id] = {}
		FIGHT_LOGS[room][char_id]['attack'] = body['attack']
		FIGHT_LOGS[room][char_id]['defence'] = body['defence']
		test('step')
		if not opponent_id in FIGHT_LOGS[room]: # если еще нет хода от оппонента
			print('Жду ответа другого игрока')
			return [json.dumps({'result': 'waiting'}).encode()]
		else:
			print('Все готово для расчетов')
			calc_step(room, char_id, opponent_id)
			if USERS[char_id].character.hp < 0 or USERS[opponent_id].character.hp < 0:
				if USERS[char_id].character.hp > USERS[opponent_id].character.hp:
					winner = 'player_1'
				else:
					winner = 'player_2'
				return [json.dumps({'result': 'finish', 'winner': winner}).encode()]
			else:
				player_1 = USERS[char_id].character.dump()
				player_2 = USERS[opponent_id].character.dump()
				result = {'result':
								{'player_1': player_1,
								 'player_2': player_2}}
				return [json.dumps(result).encode()]
	else:
		if not opponent_id in FIGHT_LOGS[room]: # если еще нет хода от оппонента
			return [json.dumps({'result': 'waiting'}).encode()]
		else:
			calc_step(room, char_id, opponent_id)
			if USERS[char_id].character.hp < 0 or USERS[opponent_id].character.hp < 0:
				if USERS[char_id].character.hp > USERS[opponent_id].character.hp:
					winner = 'player_1'
				else:
					winner = 'player_2'
				return [json.dumps({'result': 'finish', 'winner': winner}).encode()]
			else:
				player_1 = USERS[char_id].character.dump()
				player_2 = USERS[opponent_id].character.dump()
				result = {'result':
								{'player_1': player_1,
								 'player_2': player_2}}
				return [json.dumps(result).encode()]


def application(environ, start_response):
	path = environ['PATH_INFO']
	if path in ROUTES:
		app = ROUTES[path]
		return app(environ, start_response)
	return not_found(environ, start_response)

ROUTES = {
	'/':index,
	'/styles.css':styles,
	'/index.js':javascript,
	'/lobby.js':lobby_js,
	'/character/create':character_create,
	'/lobby':lobby,
	'/ask':ask,
	'/game':game,
	'/index_game.js':index_game,
	'/body.png':send_img,
	'/game/first_ask':first_stat_ask,
	'/step':step,
	'/step/waiting':waiting}


port = 8000
httpd = make_server('', port, application)
print("Serving on port {0}...".format(port))
httpd.serve_forever()

