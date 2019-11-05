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

frame_width_resize = 450

# Need to initialise frame and last frame at start to get SSIM reading
frame = fvs.read()
frame = imutils.resize(frame, width=frame_width_resize)
last_frame = frame
ssimValue = 0

time_list = []
ssim_list = []

# loop over frames from the video file stream
while (fvs.more() and (datetime.now() - start_time).seconds <= 10):
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
    frame = fvs.read()
    frame = imutils.resize(frame, width=frame_width_resize)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = np.dstack([frame, frame, frame])


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

    print("SSIM {}".format(ssimValue))

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

plt.figure()

plt.xlabel("Time")
plt.ylabel("SSIM against last frame")
plt.ylim([0, 1])
plt.yscale('linear')
plt.grid(True)
plt.plot(time_list, ssim_list)
plt.savefig('plot.png')
if (monitorAvailable):
    plt.show()
