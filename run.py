import config
from scripts import forEachImage
from scripts import detectPedestrianOnImage
import cv2


def test(a, b="a"):
    print(a, b)


trackers = cv2.MultiTracker_create()
cascade = cv2.CascadeClassifier(config.CASCADE_PATH)
tracker = cv2.TrackerCSRT_create
# tracker = cv2.TrackerKCF_create
# tracker = cv2.TrackerBoosting_create
# tracker = cv2.TrackerMIL_create
# tracker = cv2.TrackerTLD_create
# tracker = cv2.TrackerMedianFlow_create
# tracker = cv2.TrackerMOSSE_create

forEachImage(
    config.IMAGES_DIRECTORY,
    detectPedestrianOnImage,
    {"cascade": cascade, "tracker": tracker, "trackers": trackers},
)

# folderFunction=test, folderFunctionArgs = {'a':'a', "b":"b"}
