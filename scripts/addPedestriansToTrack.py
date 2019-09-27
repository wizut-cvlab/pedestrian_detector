import cv2
from .drawBoxes import drawBoxes


def addPedestriansToTrack(image, trackers, tracker):
    markedObjects = 0
    while True:
        manualMarking = cv2.selectROI("Mark pedestrian to track", image)
        if manualMarking != (0, 0, 0, 0):
            markedObjects = markedObjects + 1
            trackers.add(tracker(), image, manualMarking)
            drawBoxes(image, [manualMarking])
        print("Hit Enter to continue")
        print("Hit any other key to add next object")
        key = cv2.waitKey(0)
        cv2.destroyWindow("Mark pedestrian to track")
        if key == ord("\r"):
            return [trackers, markedObjects]
