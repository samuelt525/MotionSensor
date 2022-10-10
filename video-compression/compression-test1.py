#!/usr/bin/python3

import cv2
import sys
import os

# Exception handling
#argument check
if len(sys.argv) != 3:
	raise Exception('Invariant Number of Arguments passed.Please pass one video path and one compress percentage')

#file type check
t = str(sys.argv[1]).split(".")
if t[1].casefold() not in ["mp4", "wav"]:
	raise Exception('Raise Exception incompatible file type only mp4 or wav required')

#range of compression check
if int(sys.argv[2]) not in range(1,100):
	raise Exception('Compress percent should be in range 1-99')

# file existence check
if not os.path.exists(sys.argv[1]):
	raise Exception('the video file does not exists or the path is incorrect')


# resizing all frames
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim)


# getting video and then processing it and saving in filename_ouput.mp4
cap = cv2.VideoCapture(str(sys.argv[1]))

width  = (cap.get(3) * int(sys.argv[2]))/ 100
height = (cap.get(4) * int(sys.argv[2]))/ 100

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(total_frames)

# fourcc = cv2.VideoWriter_fourcc(*"MJPG")

out_video = cv2.VideoWriter(t[0]+'_compressed_'+sys.argv[2]+'.mp4',0x7634706d, 20.0, (int(width), int(height)),True)

frame_counter = 1

while(cap.isOpened()):

    if frame_counter % 30 == 0:
        print(str(frame_counter) + '/' + str(total_frames))
    frame_counter += 1

    ret, frame = cap.read()
    if ret:
        frameX = rescale_frame(frame,int(sys.argv[2]))
        out_video.write(frameX) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()