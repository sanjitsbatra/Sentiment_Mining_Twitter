import sys

def sort(f):
	l=open(f).read().split('\n')
	g=open('bigram-sorted','w')
	l=sorted(l)
	for i in l:
		g.write('%s\n' % i)
	g.close()

def main(file):
	sort(file)
	
main(sys.argv[1])		
