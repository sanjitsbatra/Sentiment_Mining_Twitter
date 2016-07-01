from custom.slang2english import s2e
from nltk.stem.lancaster import LancasterStemmer as LS
import re

mFile="evaluate/messages.list"
uFile="data/bigrams"

msgs=map(lambda a:a.strip(), open(mFile).readlines())

stem = LS().stem

di={}

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

for sentence in msgs:
	sentence=s2e(sentence)
	words = list(re.findall(r'[a-zA-Z]+', sentence))
	words=filter(lambda a:a not in stopwords,words)
	words = map(stem, words)
	bigram_list=[]
	for l in range(len(words)-1):
		bigram_list.append(words[l]+" "+words[l+1])
	words=bigram_list

	for w in words:
		try:
			di[w]=di[w]+1
		except:
			di[w]=1
	
arr=[]
for k in di.keys():
	arr.append((k,di[k]))
	arr=sorted(arr,key=lambda a:a[1],reverse=True)

arr=map(lambda a:str(a[0])+"\n",arr)

open(uFile,'w').writelines(arr)