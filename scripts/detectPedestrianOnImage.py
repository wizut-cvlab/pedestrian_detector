import config
import cv2
from .addPedestriansToTrack import addPedestriansToTrack
from .drawBoxes import drawBoxes


def detectPedestrianOnImage(image, previousResults, cascade, trackers, tracker):
    (trackingSuccess, trackingBoxes) = trackers.update(image)
    trackedObjects = len(trackingBoxes)
    drawBoxes(image, trackingBoxes)
    key = cv2.waitKey(config.DISPLAY_FRAME_IN_MILLISEC)
    if (
        previousResults == {}
        or key == ord(" ")
        or (
            "trackingObjects" in previousResults
            and previousResults["trackingObjects"] != trackedObjects
        )
    ):
        [trackers, trackedObjects] = addPedestriansToTrack(image, trackers, tracker)
    detections = cascade.detectMultiScale(image, 1.02, 3)
    drawBoxes(image, detections, (255, 0, 0))

    # trackedObject = GroundTruth
    # detections - test

    cv2.imshow("detections", image)
    return {"trackingObjects": trackedObjects}
