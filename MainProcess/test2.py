from functools import partial 
from threading import Thread
import multiprocessing
import time
 
def singleCount(cnt,name):
    for i in range(1,10000001):
        cnt += 1
        if(i%2500000 == 0):
            print(name,":",i)
 
lists = ['1','2','3','4']
# single process start
cnt = 0
print(" # # SINGLE PROCESSING # # ")
start_time = time.time()
for each in lists:
    singleCount(cnt,each)
print("SINGLE PROCESSING TIME : %s\n" %(time.time()-start_time))
 
# multi process start
cnt = 0
print(" # # MULTI PROCESSING # # ")
start_time = time.time()
pool = multiprocessing.Pool(processes=4)
func = partial(singleCount, cnt)
pool.map(func, lists)
pool.close()
pool.join()
print("MULTI PROCESSING TIME : %s\n" %(time.time()-start_time))
 
#multi threading start
cnt = 0
print(" # # MULTI THREADING # # ")
start_time = time.time()
th1 = Thread(target=singleCount, args=(cnt,"1"))
th1.start()
th1.join()
th2 = Thread(target=singleCount, args=(cnt,"2"))
th2.start()
th2.join()
th3 = Thread(target=singleCount, args=(cnt,"3"))
th3.start()
th3.join()
th4 = Thread(target=singleCount, args=(cnt,"4"))
th4.start()
th4.join()
print("MULTI THREADING TIME : %s\n" %(time.time()-start_time))
