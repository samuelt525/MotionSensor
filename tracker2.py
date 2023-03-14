import cv2
from tqdm import tqdm
import os

if os.path.exists("./output_video.mp4"):
    os.remove("./output_video.mp4")
if os.path.exists("./skip_output_video.mp4"):
    os.remove("./skip_output_video.mp4")

# Create a video capture object
cap = cv2.VideoCapture('./C0078_720p60_40s.mp4')

# enable OpenCV CPU multithreading
cv2.setUseOptimized(True)
cv2.setNumThreads(8) # you can adjust this number to your system specs

# Get the video properties
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

motion_threshold = 0.05 * (height * width)
motion_stats = []
print(f'total pixels = {width*height}, motion_threshold={0}')

# Create a video writer object to output the processed video
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
skip = cv2.VideoWriter('skip_output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize variables for motion detection
no_motion_frames = 0
skip_frame_counter = 0
output_frame_counter = 0
scale_factor = min(1280/width, 720/height)

# Create a background subtractor object
back_sub = cv2.createBackgroundSubtractorMOG2()

# Initialize the tqdm progress bar
progress_bar = tqdm(total=frame_count)

# Loop through all frames in the video
for i in range(frame_count):

    # Update the tqdm progress bar
    progress_bar.update(1)

    # Read the current frame
    ret, frame = cap.read()

    if not ret:  # check if the frame is empty
        continue

    frame = cv2.resize(frame, (int(width*scale_factor), int(height*scale_factor)))
    
    # Apply background subtraction to the current frame
    fg_mask = back_sub.apply(frame)

    # Remove noise from the foreground mask
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

    # Count the number of non-zero pixels in the foreground mask
    motion_count = cv2.countNonZero(fg_mask)
    motion_stats.append(motion_count)

    # If there is motion in the frame, reset the no motion frames counter
    if motion_count > 14000:
        no_motion_frames = 0
        # Draw a rectangle around the areas with motion
        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    else:
        no_motion_frames += 1

    # If there have been more than 10 consecutive frames with no motion, skip this frame
    if no_motion_frames > 10:
        skip_frame_counter += 1
        skip.write(frame)
        continue

    # Write the current frame to the output video
    out.write(frame)
    output_frame_counter += 1

# Close the tqdm progress bar
progress_bar.close()

motion_stats_mean = sum(motion_stats) / len(motion_stats)
print(round(motion_stats_mean, 1), '0.05='+str(round(0.05*motion_stats_mean, 1)), '0.5='+str(round(0.5*motion_stats_mean, 1)))

# Release the video capture and writer objects
cap.release()
out.release()
skip.release()

# Get the number of frames in the output video
output_frame_count = int(out.get(cv2.CAP_PROP_FRAME_COUNT))

# Print the number of frames in the output video
print(f'orignal frame count: {frame_count}')
print(f"out frame counter = {output_frame_counter}")
print(f"skip frame counter = {skip_frame_counter}")
print(f'skip frame percent = {round((skip_frame_counter/frame_count)*100, 1)}')