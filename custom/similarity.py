#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
INSTALL
nltk - nltk.org
go to python shell
nltk.download()
download wordnet corpora
restart your python shell
'''

'''
USAGE
import similarity; para1="I have a good house"; para2="You have two good homes"; similarity.tell(para1,para2);
'''

import nltk
from nltk.corpus import wordnet
import math
import re

stopwords=nltk.corpus.stopwords.words('english')

#Takes into input two paras and returns similarity score on a scale of 0 to 1.

def tell(para1,para2):
	#Strip anything but not alphanum
	para1=re.sub(r'[^\w ]+', '', para1)
	para2=re.sub(r'[^\w ]+', '', para2)
	
	para1=para1.lower().split()
	para2=para2.lower().split()
	
	if para1==[] or para2==[]:
		return 0

	if not filter(lambda t:t.lower() not in stopwords, para1) == []:
		para1=filter(lambda t:t.lower() not in stopwords, para1)
	if not filter(lambda t:t.lower() not in stopwords, para2) == []:
		para2=filter(lambda t:t.lower() not in stopwords, para2)
	
	score=len(set(para1).intersection(para2))
	score_1=float(score)/math.sqrt(len(para2)*len(para1))
	
	para1_with_dictionary=reduce(lambda x,y:x+y, map(lambda word:[l.name for s in wordnet.synsets(word) for l in s.lemmas],para1))
	para1_with_dictionary=map(lambda ele:ele.lower(), para1_with_dictionary)
	#^^ Returns duplicated elements as well. So we need to remove the duplicates. Converting into set does that
	
	para2_with_dictionary=reduce(lambda x,y:x+y, map(lambda word:[l.name for s in wordnet.synsets(word) for l in s.lemmas],para2))
	para2_with_dictionary=map(lambda ele:ele.lower(), para2_with_dictionary)
	
	#^^ Returns duplicated elements as well. So we need to remove the duplicates. While taking intersection the same is handled

	score1=len(set(para1_with_dictionary).intersection(para2))
	score2=len(set(para2_with_dictionary).intersection(para1))

	score_2=float(max(score1,score2))/min(len(para2),len(para1))
	
	score=(score_1+score_2)/2
	return score