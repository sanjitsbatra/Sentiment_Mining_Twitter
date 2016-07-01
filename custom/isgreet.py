from slang2english import s2e

hi_greetslist=map(lambda a:a.lower().strip(),open("data/hi_greets").readlines())
bye_greetslist=map(lambda a:a.lower().strip(),open("data/bye_greets").readlines())

def is_hi (statement):
	statement=s2e(statement).strip()
	for i in hi_greetslist:
		if (i==statement) or (i+" " in statement):
			return (True,i)
	return False

def is_bye (statement):
	statement=s2e(statement).strip()
	for i in bye_greetslist:
		if (i==statement) or (i+" " in statement):
			return (True,i)
	return False

if __name__ == "__main__":
	statement=raw_input("Enter the statement:\n")

	print "Is Hi:",is_hi(statement)
	print "Is Bye:",is_bye(statement)