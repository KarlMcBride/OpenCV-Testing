# import the necessary packages
from skimage.metrics import structural_similarity
import argparse
import cv2
import imutils

import Util_MonitorClass

def GetSSIMFromFiles(filePathA, filePathB):
    imageA = cv2.imread(filePathA)
    imageB = cv2.imread(filePathB)
    return GetSSIM(imageA, imageB)

def GetSSIM(imageA, imageB):
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    #print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Show the output images if at least one monitor is present
    if (Util_MonitorClass.GetMonitorCount() > 0):
        cv2.imshow("Original", imageA)
        cv2.imshow("Modified", imageB)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)
    return score

# Call GetSSIM if called directly from command line
if __name__ == '__main__':
    print("SSIM: {}".format(GetSSIMFromFiles('Content/Ring.png', 'Content/RingX.png')))