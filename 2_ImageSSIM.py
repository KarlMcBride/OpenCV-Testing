# import the necessary packages
from skimage.metrics import structural_similarity
import argparse
import cv2
import imutils

import Util_MonitorClass
import Util_SSIM

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", default="Content/Ring.png", required=False, help="first input image")
ap.add_argument("-s", "--second", default="Content/RingX.png", required=False, help="second input image")
args = vars(ap.parse_args())

monitorAvailable = True if Util_MonitorClass.GetMonitorCount() > 0 else False

ssimValue = Util_SSIM.GetSSIMFromFiles(args["first"], args["second"], showImages=monitorAvailable, showContours=True)
print("SSIM: {}".format(ssimValue))