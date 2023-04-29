from os import listdir
from os.path import isfile, join

osfiles = [f for f in listdir('./results_os/') if isfile(join('./results_os/', f)) and f.endswith('.md')]

res = {}
for fn in osfiles:
    f = open(join('./results_os/',fn), 'rt')
    osname = fn[:-3]
    lines = f.readlines()
    f.close()
    for l in lines:
        tmp = l.split('|')
        if len(tmp)==8:
            t = tmp[1]
            if '[' in t:
                t = t[t.index('[')+1:t.index(']')]
            t = t.strip()

            if t not in res:
                res[t] = []
            try:
                res[t].append([osname, float(tmp[3]), tmp[2].strip()])
            except:
                pass

for lang in res:
    if len(res[lang]) != 0:
        print('-------------------')
        print(lang,)
        print('-------------------')
        s = sorted(res[lang], key=lambda x:x[1])
        for ss in s:
            print(ss)
        print('-------------------')
