import threading


class Queue:
    def __init__(self):
        self.queue = []
        self.q_lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(10)


    def dequeue(self):
        self.full.acquire()
        self.q_lock.acqure()
        item = self.queue.pop(0)
        self.q_lock.release()
        self.empty.release()
        return item


    def enqueue(self,item):
        self.empty.acquire()
        self.q_lock.acquire()
        self.queue.append(item)
        self.q_lock.release()
        self.full.release()
