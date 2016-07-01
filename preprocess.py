import HTMLParser
from custom.slang2english import s2e
from nltk.stem.lancaster import LancasterStemmer as LS
stem = LS().stem
import re
import pickle
from math import log

_method="Unigram"

_htmlparser = HTMLParser.HTMLParser()
unescape = _htmlparser.unescape

tFile="data/tweets"
sFile="data/smileys"

lines=[]

#UNESCAPE
for line in open(tFile):
    line = line.strip()
    try:
        lines.append(unescape(line))
    except:
        continue

print "Total Unescaped Tweets",len(lines)

#FILTER AS PER SMILEYS - INGRAINED GROUPING using SMD (smiley dictionary)
smiley_set = map(lambda a:a.split(), open(sFile).read().split("\n"))
smileys = open(sFile).read().split()
smd={}

for m in smiley_set:
	for s in m:
		smd[s]=m[0]

def checkSmiley(line):
	for s in smileys:
		if s in line:
			return True
	return False

lines=filter(lambda line:checkSmiley(line),lines)
print "Totat Tweets after smiley filtering",len(lines)

#Remove tweets with "@" and "http"
lines=filter(lambda line: "@" not in line,lines)
lines=filter(lambda line: "http" not in line,lines)
print "Totat Tweets after removing http,@",len(lines)

#Slang2English
lines=map(lambda line: line.lower(),lines)
lines=map(lambda line: s2e(line),lines)

#Stemming
lines=map(lambda line: ''.join(map(stem, re.split(r'(\w+)', line))),lines)

print "Totat Processed Tweets",len(lines)
#Make Di Di[word][smiley] i.e smiley count for each word (Includes grouping)
DI = {}
for line in lines:
	for smiley in smileys:
		if smiley not in line:
			continue

		if _method == "Unigram":
			for word in re.split(r'(\w+)', line):
				if not word.isalpha() or len(word) <= 2:
					continue
				if word not in DI:
					DI[word] = {}
				if smd[smiley] not in DI[word]:
					DI[word][smd[smiley]] = 0
				DI[word][smd[smiley]] += 1
		
		elif _method == "Bigram":
			ls_words=re.split(r'(\w+)', line)
			ls_words=filter(lambda word:word.isalpha() and len(word) > 2, ls_words)
			bigram_list=[]
			
			for l in range(len(ls_words)-1):
				bigram_list.append(ls_words[l]+" "+ls_words[l+1])
			
			for word in bigram_list:
				if word not in DI:
					DI[word] = {}
				if smd[smiley] not in DI[word]:
					DI[word][smd[smiley]] = 0
				DI[word][smd[smiley]] += 1

#sortDI(DI):
for w in DI.keys():
	DI[w]['max'] = max(DI[w][s] for s in DI[w])

def make_alpha(DI):
    alpha = {}
    for w in DI:
        for s in DI[w]:
            if s not in alpha:
                alpha[s] = 1
            else:
                alpha[s] += 1
    return alpha

def tfidf(DI, alpha):
    DIL = {}
    for w in DI:
        if w not in DIL:
            DIL[w] = {}
        for s in DI[w]:
            DIL[w][s] = (float(DI[w][s])/DI[w]['max']) * log(float(len(DI))/alpha[s])
    return DIL
	
alpha=make_alpha(DI)
DIL = tfidf(DI, make_alpha(DI))
pickle.dump(DIL, open('DIL.pickle', 'w'))
