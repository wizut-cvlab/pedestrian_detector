import cv2


def addPedestriansToTrack(image, trackers, tracker):
    markedObjects = 0
    while True:
        markedObjects = markedObjects + 1
        manualMarking = cv2.selectROI("Mark pedestrian to track", image)
        trackers.add(tracker(), image, manualMarking)
        print("Hit Enter to continue")
        print("Hit any other key to add next object")
        key = cv2.waitKey(0)
        cv2.destroyWindow("Mark pedestrian to track")
        if key == ord("\r"):
            return [trackers, markedObjects]
