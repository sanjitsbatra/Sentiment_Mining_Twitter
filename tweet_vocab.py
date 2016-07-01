import re, nltk
fd = nltk.FreqDist(re.findall(r'[a-zA-Z]+', open('tweets').read()))
for f in list(fd):
    print f, fd[f]
