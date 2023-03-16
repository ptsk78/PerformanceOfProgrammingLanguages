from os import listdir, cpu_count
from os.path import isfile, join
from datetime import datetime, date, timedelta
from dateutil import parser
import matplotlib.pyplot as plt
import pandas as pd
from prettytable import PrettyTable, MARKDOWN
import distro
import platform
from googlesearch import search

def geturl(lang, what):
    if lang == "custom c++":
        return "[custom c++](https://www.frisky.world)"
    query = "{} {}".format(lang, what)

    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        return "[{}]({})".format(lang,j)

def process(fn):
    f = open(fn, 'rt')
    lines = f.readlines()
    f.close()
    ret = []
    ret2 = []

    ret.append(fn.replace('.perf',''))
    ret2.append(fn.replace('.perf',''))
    for i in range(len(lines)-1):
        ret.append((parser.parse(lines[i+1].replace('\n',''))-parser.parse(lines[i].replace('\n',''))).total_seconds())

    ret2.append(parser.parse(lines[0].replace('\n','')))
    ret2.append(parser.parse(lines[-1].replace('\n','')))
    return ret, ret2

def readusage():
    t = []
    c = []
    m = []

    f = open('usage.txt')
    lines = f.readlines()
    f.close()

    for l in lines:
        tmp = l.split(',')
        t.append(parser.parse(tmp[0]))
        c.append(float(tmp[1]))
        m.append(float(tmp[2]))

    return t, c, m

def pickmedian(x):
    x = sorted(x, key=lambda x: x[0])

    return x[len(x)//2]

def get_name():
    info = distro.os_release_info()
    name = ''
    try:
        name = info['name']
    except:
        pass

    return name

def get_version():
    info = distro.os_release_info()
    version = ''
    try:
        version = info['version']
    except:
        pass

    return version

def distroname():
    return '{} {}\n{}'.format(geturl(get_name(), 'operating system'), get_version(), platform.platform())
    
def getLangVer(lang):
    ret = ''
    try:
        f = open(lang + '.version')
        ret = f.readline().strip().replace('\n','')
        if len(ret)==0:
            ret = f.readline().strip().replace('\n','')        
        f.close()
    except:
        pass
    
    return ret

today = date.today()
dicAll = {}
round = 0
while True:
    round += 1
    perffiles = [f for f in listdir('./') if isfile(join('./', f)) and f.endswith('.perf' + str(round))]
    if len(perffiles) == 0:
        break

    stats = []
    dic = {}
    times = []
    for fn in perffiles:
        try:
            ret, ret2 = process(fn)
            stats.append(ret)
            dic[ret2[0]] = [ret2[1], ret2[2]]
            times.append(ret2[1])
            times.append(ret2[2])
        except:
            pass


    stats = sorted(stats, key=lambda x: sum(x[1:]))

    fig, axs = plt.subplots(3)
    t, c, m = readusage()
    axs[0].plot(t, c)
    axs[0].set_ylim([0, 100])
    axs[0].set_title('CPU usage on {} ({})'.format(distroname(), today.strftime("%Y-%m-%d")))
    axs[0].set_xlim([min(times)-timedelta(seconds=1.0), max(times)+timedelta(seconds=1.0)])
    axs[1].plot(t, m)
    axs[1].set_ylim([min(m) * 0.99, max(m) * 1.01])
    axs[1].set_title('Memory usage')
    axs[1].set_xlim([min(times)-timedelta(seconds=1.0), max(times)+timedelta(seconds=1.0)])
    for d in dic:
        axs[2].plot([dic[d][0], dic[d][1]], [1, 1])
        axs[2].text(dic[d][0]+(dic[d][1]-dic[d][0])/2.0, 1.2, d[:-1], rotation='vertical')
    axs[2].set_title('Which language is running')
    axs[2].set_xlim([min(times)-timedelta(seconds=1.0), max(times)+timedelta(seconds=1.0)])
    axs[2].set_ylim([0, 3])
    axs[2].yaxis.set_visible(False) 
    plt.gcf().set_size_inches(13, 13)
    plt.savefig('cpumem' + str(round) + '.png')
    df = pd.DataFrame(stats, columns=['Language', 'Round 1', 'Round 2', 'Round 3', 'Round 4', 'Round 5'])
    df.plot(x='Language', kind='bar', stacked=False, title='Performance on {} ({})'.format(distroname(), today.strftime("%Y-%m-%d")))
    plt.gcf().set_size_inches(13, 13)
    plt.savefig('perfcomp' + str(round) + '.png')

    x = PrettyTable()
    x.field_names = ['Language', 'Adjusted Time (s)', 'Time (s)', 'CPU (%)', 'Mem (%)']
    for s in stats:
        aa = 0.0
        ac = 0.0
        am = 0.0
        for i in range(len(t)):
            if t[i] >= dic[s[0]][0] and t[i] <= dic[s[0]][1]:
                aa += 1.0
                ac += c[i]
                am += m[i]
        x.add_row([s[0], sum(s[1:])/5.0 * ac/aa / (100.0 / cpu_count()), sum(s[1:])/5.0, ac/aa, am/aa])
        if s[0][:-1] not in dicAll:
            dicAll[s[0][:-1]] = []
        dicAll[s[0][:-1]].append([sum(s[1:])/5.0 * ac/aa / (100.0 / cpu_count()), sum(s[1:])/5.0, ac/aa, am/aa])

    print(x)

results = []
for d in dicAll:
    results.append([d, pickmedian(dicAll[d])])

final = []
ff = []
for r in results:
    final.append([r[0], r[1][0], r[1][1], r[1][2], r[1][3]])
    ff.append([r[0], r[1][0]])

final = sorted(final, key=lambda s: s[1])

ff = sorted(ff, key=lambda s: s[1])
df = pd.DataFrame(ff, columns=['Language', 'Adjusted Time (seconds)'])
df.plot(x='Language', kind='bar', stacked=False, title='Performance on {} ({})'.format(distroname(), today.strftime("%Y-%m-%d")))
plt.gcf().set_size_inches(13, 13)
plt.savefig('perfcomp_final.png')

x = PrettyTable()
x.field_names = ['Language', 'Version', 'Adjusted time based on CPU usage (seconds)', 'Average time (seconds)', 'Average CPU usage[^1] (%)', 'Average memory usage[^1] (%)']
for f in final:
    x.add_row([geturl(f[0], 'programming language'), getLangVer(f[0]),"{:.3f}".format(f[1]), "{:.3f}".format(f[2]), "{:.3f}".format(f[3]), "{:.3f}".format(f[4])])
yy = 'Lower is better - on {} on {}:\n'.format(distroname(), today.strftime("%Y-%m-%d"))
print(yy)
print(x)

f = open("./results_os/{}.txt".format(get_name()), "wt")
f.write('\n')
f.write(yy)
f.write('\n')
x.set_style(MARKDOWN)
f.write(x.get_string())
f.write('\n')
f.close()
