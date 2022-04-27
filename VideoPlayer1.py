import cv2
import threading
from queue import Queue;

clipName = 'clip.mp4'

def convert_to_grayscale(producer: Queue, consumer: Queue):
    count = 0
    while True:
        inputFrame = producer.dequeue()

        if inputFrame == 'FINISHED':
            break
        grayFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        consumer.enqueue(grayFrame)
        count +=1

    consumer.enqueue('FINISHED')


def extract_frames(producer: Queue):
    clipName = 'clip.mp4'

    count = 0
    vid_capture = cv2.VideoCapture(clipName)

    reading, image = vid_capture.read()
    while reading:
        producer.enqueue(image)
        reading, image = vid_capture.read()
    producer.enqueue('FINISHED')

    
def display_frames(consumer: Queue):
    count = 0
    while True:
        frame = consumer.dequeue()

        if frame == 'FINISHED':
            break
        cv2.imshow('Video', frame)

        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    cv2.destroyAllWindows()


producerQ = Queue()
consumerQ = Queue()

producer_thread = threading.Thread(target=extract_frames, args=(producerQ,))
grayscale_thread = threading.Thread(target=convert_to_grayscale, args=(producerQ, consumerQ))
consumer_thread = threading.Thread(target=display_frames, args=(consumerQ,))

producer_thread.start()
grayscale_thread.start()
consumer_thread.start()
