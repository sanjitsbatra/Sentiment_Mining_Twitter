import os, sys, json

filelist = sys.argv[1:]

log = open('log', 'w')
for file in filelist:
    fp = open(file)
    i = 0
    while True:
        try:
            di = json.loads(fp.readline())
            i += 1
            text = di.get('text')
            if text:
                print text
        except UnicodeEncodeError:
            log.write("UnicodeError: filename %s, line %d\n" %(file, i))
            continue
        except ValueError:
            log.write("File ended: filename %s, line %d\n" %(file, i))
            break
