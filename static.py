
with open('index.html', encoding='utf-8') as f:
	index = f.read()

with open('styles.css', encoding='utf-8') as f:
	styles = f.read()

with open('index.js', encoding='utf-8') as f:
	js = f.read()

with open('lobby.html', encoding='utf-8') as f:
	lobby = f.read()

with open('lobby.js', encoding='utf-8') as f:
	lobby_js = f.read()

with open('game.html', encoding='utf-8') as f:
	game = f.read()

with open('index_game.js', encoding='utf-8') as f:
	index_game = f.read()

with open('body.png', 'rb') as f:
	image = f.read()

not_found_var = '<html><h1>Page not Found</h1><p>That page is unknown. Return to the <a href="/">home page</a></p></html>'