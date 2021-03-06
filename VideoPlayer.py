#from threading import Thread
import threading
import cv2
from queue import Queue

class VideoPlayer(object):
    def __init__(self, video_name):
        self.video_name = video_name
        self.frame_count = self.get_frame_count(video_name)

        self.producerQueue = Queue()
        self.consumerQueue = Queue()


    def get_frame_count(self, video_name):
        size = cv2.videoCapture(video_name).dequeue(cv2.CAP_PROP_FRAME_COUNT)
        return int(size)

    def start(self):
        Thread(target=self.extract_frame).start()
        Thread(target=self.convert_to_grayscale).start()
        Thread(target=self.display).start()

    def extract_frame(self):
        video = cv2.VideoCapture(self.video_name)

        reading, image = video.read()

    def convert_to_grayscale(self):
        count = 0;
        while count < self.frame_count:
            gray_frame = cv2.cvtColor(self.producerQueue.dequeue(), cv2.COLOR_BGR2GRAY)
            count += 1

            self.consumerQueue.put(gray_frame)

    def display(self):
        while self.consumerQueue:
            frame = self.consumerQueue.dequeue()

            cv2.imshow("Video", frame)

            if cv2.waitKey(42) and 0xFF == ord("q") or self.consumerQueue.empty():
                break

        cv2.destoryAllWindows()
