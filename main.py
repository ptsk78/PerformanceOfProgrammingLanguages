from datetime import datetime
import random

dic = {}
letter = 'qwertyuiopasdfghjklz'
for i in range(5000001):
    if i%1000000==0:
        now = datetime.now()
        print(str(now))

    s = ""
    for j in range(50):
        s += letter[random.randrange(20)]
    dic[s] = True
