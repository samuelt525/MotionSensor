#!/usr/bin/python3

import cv2
import sys
import os
from alive_progress import alive_bar
import time

from threading import Thread
from queue import Queue
from imutils.video import FPS

# USAGE
# python compression-test2.py input_filename.mp4 int<rescale_ratio> int<output_fps>

class FileVideoStream:
    def __init__(self, path, queueSize=100):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False

        # initialize the queue used to store frames read from the video file
        self.Q = Queue(maxsize=queueSize)

    # start a thread to read frames from the file video stream
    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()
                # if the `grabbed` boolean is `False`, then we have reached the end of the video file
                if not grabbed:
                    self.stop()
                    return
                # add the frame to the queue
                self.Q.put(frame)

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

def compression_test(argv):
    # Exception handling

    # argument check
    print(argv)
    if len(argv) != 4:
        raise AttributeError('Check Args!')

    # file type check
    t = str(argv[1]).split(".")
    if t[-1].casefold() not in ["mp4", "wav"]:
        print(t)
        raise TypeError(
            'Raise Exception incompatible file type only mp4 or wav required')

    # range of compression check
    if int(argv[2]) not in range(1, 100):
        raise TypeError('Compress percent should be in range 1-99')

    # file existence check
    if not os.path.exists(argv[1]):
        raise FileNotFoundError(
            'the video file does not exists or the path is incorrect')

    # resizing all frames
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim)

    # getting video and then processing it and saving in filename_ouput.mp4
    fps = FPS().start()
    fvs = FileVideoStream(str(sys.argv[1])).start()

    time.sleep(1.0)

    width = (fvs.stream.get(3) * int(sys.argv[2])) / 100
    height = (fvs.stream.get(4) * int(sys.argv[2])) / 100

    total_frames = int(fvs.stream.get(cv2.CAP_PROP_FRAME_COUNT))

    print('\nTotal Frames: ' + str(total_frames) + ', Original Resolution: ' + str(int(fvs.stream.get(3))) +
        'x' + str(int(fvs.stream.get(4))) + ', Scaled Resolution: ' + str(int(width)) + 'x' + str(int(height)) + '\n')

    out_video = cv2.VideoWriter(t[0] + '_rescale' + argv[2] + '_fps_' + argv[3] + str(
        time.time()) + '.mp4', 0x7634706d, float(argv[3]), (int(width), int(height)), True)

    with alive_bar(total_frames) as bar:
        while fvs.more():

            bar()

            # grab the frame from the threaded video file stream, resize
            # it, and convert it to grayscale (while still retaining 3
            # channels)
            frame = fvs.read()
            # frame = imutils.resize(frame, width=450)
            # frame = cv2.cvtColorpip install --upgrade scenedetect[opencv]
(frame, cv2.COLOR_BGR2GRAY)

            # frame = np.dstack([frame, frame, frame])

            frame = rescale_frame(frame, int(argv[2]))
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # frame = cv2.GaussianBlur(src=frame, ksize=(5, 5), sigmaX=0)

            # display the size of the queue on the frame
            # cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
            #             (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # show the frame and update the FPS counter
            # cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            fps.update()

    fps.stop()

    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()

if __name__ == '__main__':
    compression_test(sys.argv)
