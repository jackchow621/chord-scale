import threading
import time
from queue import Queue


class MyThread(threading.Thread):
    def __init__(self, evt, queue):
        threading.Thread.__init__(self)
        # 初始化
        self.evt = evt
        self.queue = queue
        self.index = 0

    def play(self,i):
        print('playing', i,time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time())))
        time.sleep(1)

    def run(self):
        while self.index <20:
            if self.queue.empty():
                self.play(self.index)
                self.index+=1
            else:
                q = self.queue.get()
                print('receving a stop signal',time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time())))
                self.evt.wait()

class MyThread2(threading.Thread):
    def __init__(self, evt, queue):
        threading.Thread.__init__(self)
        # 初始化
        self.evt = evt
        self.queue = queue

    def run(self):
        '''time.sleep(2)
        print('user click stop button')
        self.queue.put(0)

        time.sleep(4)
        print('user click play button')
        self.evt.set()

        time.sleep(5)
        print('user click stop button again')
        self.queue.put(0)

        time.sleep(6)
        print('user click play button again')
        self.evt.set()'''
        pass

if __name__ == "__main__":
    # 初始 为 False
    q = Queue()
    evt = threading.Event()
    thread1 = MyThread(evt, q)
    thread1.start()
    thread2 = MyThread2(evt,q)
    thread2.start()

    time.sleep(2)
    print('user click stop button',time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time())))
    thread2.queue.put(0)

    time.sleep(4)
    print('user click play button',time.strftime('%Y.%m.%d.%H.%M.%S',time.localtime(time.time())))
    thread2.evt.set()
