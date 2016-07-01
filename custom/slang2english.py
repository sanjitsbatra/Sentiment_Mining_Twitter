import re, string
from spell_correct import correct

li = map(lambda i: i.split("\t", 1),open("data/slang_dict").read().split("\n"))

di = {}
for m in li[:-1]:
    if len(m) != 2:
        print li.index(m), m
    di[m[0].strip()] = m[1].strip()

slangset = set(di.keys())

#print len(slangset)

def s2e(s):
    d = {}
    splitted_s = re.split(r'(\w+)', s)
    for i, word in enumerate(splitted_s):
        if word.strip() and word in slangset:
            ##splitted_s[i] = correct(di[word])
			##Disable slang2english transformations
			splitted_s[i] = correct(word)
    return string.join(splitted_s, "")
    
if __name__ == '__main__':
    print s2e("whr r u")
