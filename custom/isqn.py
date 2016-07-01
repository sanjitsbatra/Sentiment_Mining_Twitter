import sys
from slang2english import s2e

def nt(s):
	s1=s.split(' ')
	if (len(s1[0])>3) and (( (s1[0][-3:]=="n't") or (s1[0][-3:]=="'nt") )) :
		s=str(s1[0][:-3]) + ' ' + str(s1[1])
	elif (len(s1[0])>2) and (s1[0][-2:]=="nt") :
		s=str(s1[0][:-2]) + ' ' + str(s1[1])
	elif (len(s1[1])>3) and ( (s1[1][-3:]=="n't") or (s1[1][-3:]=="'nt") ) :
		s=str(s1[0]) + ' ' + str(s1[1][:-3])
	elif (len(s1[1])>2) and (s1[1][-2:]=="nt") :
		s=str(s1[0]) + ' ' + str(s1[1][:-2])
	return s	 

def bigram(a):
	b=[' '] * ( len ( a.split(' ') ) -1 )
	for i in range( len( a.split( ' ' ) ) -1 ):
		b[i] = ' '.join(a.split(' ')[i:i+2])
		b[i] = nt(b[i])
	return b

bigramlist=open('data/bigram-sorted').read().split('\n')	
unigramlist=open('data/unigram').read().split('\n')	

def is_qn(s):
	reason=None
	s1=s2e(s.lower())
	
	#Return false in case of empty string
	if s1.replace(" ","").strip() == "" or s1.replace(" ","").strip() == "there?":
		return False
	
	cn=0
	if len(s1)>1:
		if  (s1[-1]=='?'):
			cn+=1
			return (True,"Q")
	
	elif ( len(s1.split(' '))<2 ):	
		cn+= ((s1 in unigramlist)>0)
		if cn>0:
			return (True,"From Unigram")
	
	else:
		cn+=((reduce(lambda x,y : (x|y) , map( lambda x: (x in bigramlist), bigram(s1))))>0 ) 
		if cn>0:
			return (True,"From Bigram")
		
	return False
	
if __name__ == "__main__":
	s=raw_input("Enter the statement:\n")
	print is_qn(s)
