import config
import cv2

from .addPedestriansToTrack import addPedestriansToTrack
from .calculateIOU import calculateIOU
from .drawBoxes import drawBoxes


def detectPedestrianOnImage(image, previousResults, cascade, tracker):
    if "trackers" in previousResults:
        trackers = previousResults["trackers"]
        (trackingSuccess, trackingBoxes) = trackers.update(image)
        trackedObjectsNum = len(trackingBoxes)
        drawBoxes(image, trackingBoxes)
    else:
        trackers = None
        trackedObjectsNum = 0
        trackingBoxes = []
    key = cv2.waitKey(config.DISPLAY_FRAME_IN_MILLISEC)
    if (
        previousResults == {}
        or key == ord(" ")
        or (
            "trackingObjects" in previousResults
            and previousResults["trackingObjects"] != trackedObjectsNum
        )
    ):
        [trackers, trackedObjectsNum] = addPedestriansToTrack(
            image, tracker, trackers, trackedObjectsNum
        )
    detections = cascade.detectMultiScale(image, 1.02, 3)
    drawBoxes(image, detections, (255, 0, 0))
    [cumulativeIOU, properlyDetectedObjects, objectsIOU] = calculateIOU(
        detections, trackingBoxes, config.MINIMUM_IOU
    )
    detectedObjects = len(detections)
    if detectedObjects > 0:
        meanIOU = cumulativeIOU / detectedObjects
    else:
        meanIOU = 0
    cv2.imshow("detections", image)
    wrongDetections = detectedObjects - properlyDetectedObjects
    print(properlyDetectedObjects, trackedObjectsNum, wrongDetections, meanIOU)
    return {
        "trackingObjects": trackedObjectsNum,
        "properlyDetectedObjects": properlyDetectedObjects,
        "trackers": trackers,
        "wrongDetections": wrongDetections,
        "meanIOU": meanIOU,
    }
