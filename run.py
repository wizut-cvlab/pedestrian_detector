import cv2
import config
from scripts import detectPedestrianOnImage
from scripts import forEachImage
from scripts import saveResults

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
    {"cascade": cascade, "tracker": tracker},
    saveResults,
    {"resultsFolder": config.RESULTS_FOLDER},
)
