import glob,json

di = {}
index = 0
lfile = open('location', 'w')
for name in glob.glob('data/set*'):
	f = open(name)
	for line in f:
		index += 1
		print str(index/14366169.0)+"\r",
		try:
			js = json.loads(line)
		except:
			continue
		if 'user' not in js:
			continue
		loc = js['user']['location']
		#loc2 = js['place']
		if not loc:
			continue
		if loc not in di:
			di[loc] = 1
		else:
			di[loc] += 1		
		#print loc
		#if loc:
		#	lfile.write(loc+'\n')
keys=sorted(di.keys(), key=lambda i: di[i])
for key in keys:
	print key, di[key]
