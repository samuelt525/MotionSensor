#!/usr/bin/python3

import cv2
import sys
import os


## USAGE
# python compression-test1.py input_filename.mp4 int<rescale_ratio> int<output_fps>


# Exception handling
#argument check
if len(sys.argv) != 4:
	raise Exception('Check Args!')

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

out_video = cv2.VideoWriter(t[0]+'_rescale'+sys.argv[2]+'_fps'+sys.argv[3]+'.mp4',0x7634706d, float(sys.argv[3]), (int(width), int(height)),True)

frame_counter = 1

while(cap.isOpened()):

    if frame_counter % 60 == 0:
        print(str(frame_counter) + '/' + str(total_frames))
    frame_counter += 1

    ret, frame = cap.read()

    if ret:
        if frame_counter % float(sys.argv[3]) == 0:
            print('here')
            # Prepare image; rescale, grayscale and blur
            prepared_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            prepared_frame = rescale_frame(frame, int(sys.argv[2]))
            prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
            out_video.write(prepared_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()