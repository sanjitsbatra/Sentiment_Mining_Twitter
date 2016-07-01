from emotions import Emotions
from custom.slang2english import s2e
from custom.isqn import is_qn
from custom.isgreet import is_hi,is_bye

choice = raw_input( ''' Enter your choice\n
1. Find emotion\n
2. Find Question Type\n
3. Find if isGreet\n
4. Slang2Dict\n''' )

if int(choice) == 1:
	e = Emotions()
	ctr=True
	while ctr:
		statement=raw_input("Enter emotional sentence: ")
		if statement.strip()=="e":
			msgs=map(lambda a:a.strip(), open(mFile).readlines())
			lines=[]
			for m in msgs:
				em=e.predict(m)
				lines.append('"'+m.replace('"',"'")+'",'+str(em[0])+","+str(em[1])+"\n")
				
			open(meFile,'w').writelines(lines)
			ctr=False
		else:
			print e.predict(statement)

elif int(choice) == 2:
	while True:
		statement=raw_input("Enter emotional sentence: ")
		print is_qn(statement);
		
elif int(choice) == 3:
	while True:
		statement=raw_input("Enter emotional sentence: ")
		print is_hi(statement);
		print is_bye(statement);

elif int(choice) == 4:
	while True:
		statement=raw_input("Enter emotional sentence: ")
		print s2e(statement)