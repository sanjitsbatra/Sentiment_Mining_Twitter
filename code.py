import json

f = open('locations', 'w')
g = open('out', 'w')
while True:
	try:
		inp = raw_input()
	except:
		break
	ijs = json.loads(inp)
	if 'user' not in ijs:
		continue
	location = ijs['user']['location']
	text = ijs['text']
	f.write(location+"\n")
	if location == 'England':
		g.write(text+'\n')
