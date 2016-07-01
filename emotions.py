import pickle, re
from nltk.stem.lancaster import LancasterStemmer as LS
from custom.slang2english import s2e
from custom.isqn import is_qn
from custom.isgreet import is_hi,is_bye

_method="Unigram"

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

stopset = set(stopwords)

sFile="data/smileys"
mFile="evaluate/messages.list"
meFile="evaluate/messages.csv"
emo_words_file="data/emo_words.csv"

smiley_set = map(lambda a:a.split(), open(sFile).read().split("\n"))

stem = LS().stem

def combine_p(a):
	b=""
	for i in range(len(a)-1):
		b+=a[i]
	return (b,a[len(a)-1].strip())

class Emotions():
	def __init__(self):
		self.DIL = pickle.load(open('DIL.pickle'))
		self.emo_words = map(lambda a:combine_p(a.split(",")),open(emo_words_file).readlines())

	def predict(self, sentence):
		sm_vector=filter(lambda s:filter(lambda a:a in sentence.lower(), s),smiley_set)
		
		if is_hi(sentence):
			return ("Hi",is_hi(sentence)[1])
		
		if is_bye(sentence):
			return ("Bye",is_bye(sentence)[1])

		if is_qn(sentence):
			return ("Q",is_qn(sentence)[1])
		
		num_smileys=len(sm_vector)

		if num_smileys==1:
			return (sm_vector[0][0],"Only one type of smiley")

		elif num_smileys>1:
			return (None,"More than one type of smileys")

		if ("not " in sentence) or ("n't " in sentence):
			return (None,"Unsure because of negation")
			
		for e in self.emo_words:
			if e[0] in sentence:
				return (e[1],"short circuit")

		DIL = self.DIL
		L = []
		P = []

		sentence=s2e(sentence)
		for e in self.emo_words:
			if e[0] in sentence:
				return (e[1],"short circuit")

		words = list(re.findall(r'[a-zA-Z]+', sentence))
		words = map(stem, words)
		
		if _method == "Bigram":
			bigram_list=[]
			for l in range(len(words)-1):
				bigram_list.append(words[l]+" "+words[l+1])
			words=bigram_list

		print words
		words = filter(lambda w: stem(w) in DIL and w not in stopset, words)
		print words
		
		if words==[]:
			return (None,"No words to evaluate")

		#CONTINUE FROM HERE
		def p(w):
			return sorted([(x, DIL[w][x]) for x in DIL[w].keys()], key=lambda i:i[1], reverse=True)
		
		arr=[]

		'''
		def variance(arr):
			if len(arr) == 1:
				return arr[0]

			mean=sum(arr)/len(arr)
			return sum(map(lambda a:pow(a-mean,2),arr))/len(arr)


		for smiley in DIL[words[0]].keys():
			sm_vector=[]
			for w in words:
				try:
					sm_vector.append(DIL[w][smiley])
				except KeyError:
					#As for a word some smileys may not exist at all
					pass
			arr.append((smiley,variance(sm_vector)))
			arr.sort(key=lambda a:a[1],reverse=True)
		
		return arr[0]
		''''''

		'''
		dis = {w: p(w) for w in words}
		disli = [(w, dis[w]) for w in dis]
		disli.sort(key=lambda i: i[1][0][1], reverse=True) #For each word, 1 (the second part of tuple) => 0 (first smiley for the word as already sorted) => 1 (the score of the tuple))

		if disli:
			return (disli[0][1][0][0], disli[0][0])
		else:
			return (None,None)
		'''
		'''

if __name__ == '__main__':
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
