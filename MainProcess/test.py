import time
import os

from multiprocessing import Pool
import multiprocessing as mp




def do_work(x) :
    print('value',x, '에 대학 적업 PID = ', os.getpid())
    time.sleep(3);
    return x*x

if __name__ == '__main__':
  
    print("Number of Processors: ", mp.cpu_count())
    pool = Pool(5)
    start_time = int(time.time())

    print(pool.map(do_work,range(0,10)))
    print('seconds: &s', time.time() - start_time)

    pool.join