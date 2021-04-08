from datetime import datetime
from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import numpy as np
import time
import cv2

import Util_MonitorClass

# Import custom Python files from relative directories
# As it's relative, you must run this file from within its directory

monitorCount = Util_MonitorClass.GetMonitorCount()

# start the file video stream thread and allow the buffer to
# start to fill
print("[INFO] starting video file thread...")
fvs = FileVideoStream("rtsp://192.168.1.245:554/videoStreamId=1").start()
time.sleep(1.0)

# start the FPS timer
fps = FPS().start()

start_time = datetime.now()

run_time = 0
prev_run_time = 0

# loop over frames from the video file stream
while (fvs.more() and (datetime.now() - start_time).seconds <= 10):
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
    frame = fvs.read()
    frame = imutils.resize(frame, width=450)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = np.dstack([frame, frame, frame])

    # display the size of the queue on the frame
    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    run_time = (datetime.now() - start_time).seconds
    if (run_time > prev_run_time):
        print("Run Time: {}".format(run_time))
        prev_run_time = run_time
    # Display remaining run time
    cv2.putText(frame, "Run Time: {}".format(run_time),
        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # show the frame and update the FPS counter
    # Don't show when running on Jenkins/via SSH, as there's no UI.
    # Doing so will result in a "cannot connect to X server" error.
    if (monitorCount > 0):
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
    fps.update()


