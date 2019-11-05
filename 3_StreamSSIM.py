from datetime import datetime
from imutils.video import FileVideoStream
from imutils.video import FPS
from matplotlib import pyplot as plt

import copy
import imutils
import numpy as np
import time
import cv2

import Util_MonitorClass
import Util_SSIM


# Control variables - impact performance and event detection
consecutive_frames_for_lock_unlock = 5  # Number of frames to take average of to detect lock - reduces flip flopping
frame_width_resize = 450                # Frame width in pixels - smaller size reduces processing duration
locked_ssim_trigger = 0.9999            # running SSIM average above this amount will log a "locked" event, below will clear it
record_duration_time_secs = 120         # recording time in seconds


def detect_locked_stream(last_x_list, lock_detected):
    global locked_events
    total_ssim = 0
    for ssim in last_x_list:
        total_ssim += ssim
    average_ssim = total_ssim / len(last_x_list)
    if (average_ssim > locked_ssim_trigger and lock_detected == False):
        print("Lock detected: {}".format(datetime.now()))
        lock_detected = True
        locked_events += 1
    elif (average_ssim < locked_ssim_trigger and lock_detected == True):
        print("Recovered    : {}".format(datetime.now()))
        lock_detected = False
    return lock_detected


monitorAvailable = True if Util_MonitorClass.GetMonitorCount() > 0 else False

# start the file video stream thread and allow the buffer to
# start to fill
print("[INFO] starting video file thread...")
fvs = FileVideoStream("http://192.168.1.134:8081").start()
time.sleep(1.0)

# start the FPS timer
fps = FPS().start()

start_time = datetime.now()

run_time = 0
prev_run_time = 0

locked_events = 0
locked_frames = 0
total_frames = 0

# Need to initialise frame and last frame at start to get SSIM reading
frame = fvs.read()
frame = imutils.resize(frame, width=frame_width_resize)
last_frame = frame
ssimValue = 0

time_list = []
ssim_list = []

lock_detected = False

# Create video writer instance
frame_height, frame_width, channels = frame.shape
recording_file = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width, frame_height))

# loop over frames from the video file stream
while (fvs.more() and (datetime.now() - start_time).seconds <= record_duration_time_secs):
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
    frame = fvs.read()
    frame = imutils.resize(frame, width=frame_width_resize)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = np.dstack([frame, frame, frame])

    # Write the frame into the file 'output.avi'
    recording_file.write(frame)

    run_time = (datetime.now() - start_time).seconds
    if (run_time > prev_run_time):
        #print("Run Time: {}".format(run_time))
        prev_run_time = run_time


    # Copy the current frame, as the SSIM operation modifies what's passed in
    current_frame = copy.deepcopy(frame)
    ssimValue = Util_SSIM.GetSSIM(frame, last_frame, showImages=False, showContours=False)
    last_frame = copy.deepcopy(current_frame)

    time_list.append(datetime.now())
    ssim_list.append(ssimValue)

    #print("SSIM {}".format(ssimValue))
    lock_detected = detect_locked_stream(ssim_list[-consecutive_frames_for_lock_unlock:], lock_detected)
    if (lock_detected):
        locked_frames += 1
    total_frames += 1

    # show the frame and update the FPS counter
    # Don't show when running on Jenkins/via SSH, as there's no UI.
    # Doing so will result in a "cannot connect to X server" error.
    if (monitorAvailable):
        annotated_frame = frame
        # Display the size of the queue on the frame
        cv2.putText(annotated_frame, "Queue Size: {}".format(fvs.Q.qsize()),
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # Display remaining run time
        cv2.putText(annotated_frame, "Run Time: {}".format(run_time),
            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(annotated_frame, "SSIM: {}".format(ssimValue),
            (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("annotated_frame", annotated_frame)
        cv2.waitKey(1)
    fps.update()

recording_file.release()

percentage_locked_frames = (locked_frames * 100) / total_frames
print("Total Frames : {} ".format(total_frames))
print("Locked Frames: {} ".format(locked_frames) + "({0:.2f}%)".format(percentage_locked_frames))
print("Locked Events: {} ".format(locked_events))


plt.figure()
plt.xlabel("Time")
plt.ylabel("SSIM against last frame")
plt.ylim([0, 1.1])
plt.yscale('linear')
plt.grid(True)
plt.plot(time_list, ssim_list)
plt.savefig('plot.png')
if (monitorAvailable):
    plt.show()