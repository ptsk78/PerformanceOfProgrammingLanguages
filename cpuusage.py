import psutil
import time
from datetime import datetime

while True:
    f = open("usage.txt", "at")
    now = datetime.now()
    f.write("{},{},{}\n".format(str(now), psutil.cpu_percent(), psutil.virtual_memory().percent))
    f.close()
    time.sleep(0.03)



