import cv2
from .drawBoxes import drawBoxes


def addPedestriansToTrack(image, tracker, trackers, trackedObjectsNum):
    if trackers == None:
        trackers = cv2.MultiTracker_create()
    markedObjects = trackedObjectsNum
    while True:
        manualMarking = cv2.selectROI("Mark pedestrian to track", image)
        if manualMarking != (0, 0, 0, 0):
            markedObjects = markedObjects + 1
            trackers.add(tracker(), image, manualMarking)
            drawBoxes(image, [manualMarking])
        print("Hit Enter to continue")
        print("Hit backspace to clear all tracked objects")
        print("Hit any other key to add next object")
        key = cv2.waitKey(0)
        cv2.destroyWindow("Mark pedestrian to track")
        if key == ord("\r"):
            return [trackers, markedObjects]
        if key == 8:
            trackers = cv2.MultiTracker_create()
            markedObjects = 0
            print("!! You clear all tracked objects !!")
