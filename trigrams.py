from custom.slang2english import s2e
from nltk.stem.lancaster import LancasterStemmer as LS
import re

mFile="evaluate/messages.list"
uFile="data/trigrams"

msgs=map(lambda a:a.strip(), open(mFile).readlines())

stem = LS().stem

di={}

for sentence in msgs:
	sentence=s2e(sentence)
	words = list(re.findall(r'[a-zA-Z]+', sentence))
	words = map(stem, words)
	trigram_list=[]
	for l in range(len(words)-2):
		trigram_list.append(words[l]+" "+words[l+1]+" "+words[l+2])
	words=trigram_list

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