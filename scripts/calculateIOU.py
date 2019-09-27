def calculateIOU(detections, groundTruth, minimumIOU=0):
    cumulativeIOU = 0
    objectsIOU = []
    properlyDetectedObjects = 0
    for detectObject in detections:
        bigestIOUOfAllGroundTruthObjects = 0
        for groundTruthObject in groundTruth:
            objectIOU = 0
            # determine the (x, y)-coordinates of the intersection rectangle
            intersectionRectangleTopLeftXCoordinate = int(
                max(detectObject[0], groundTruthObject[0])
            )
            intersectionRectangleTopLeftYCoordinate = int(
                max(detectObject[1], groundTruthObject[1])
            )
            intersectionRectangleBottomRightXCoordinate = int(
                min(
                    detectObject[0] + detectObject[2],
                    groundTruthObject[0] + groundTruthObject[2],
                )
            )
            intersectionRectangleBottomRightYCoordinate = int(
                min(
                    detectObject[1] + detectObject[3],
                    groundTruthObject[1] + groundTruthObject[3],
                )
            )
            # calculate Rectangles Area
            intersectionRectangleArea = max(
                0,
                intersectionRectangleBottomRightXCoordinate
                - intersectionRectangleTopLeftXCoordinate
                + 1,
            ) * max(
                0,
                intersectionRectangleBottomRightYCoordinate
                - intersectionRectangleTopLeftYCoordinate
                + 1,
            )
            detectObjectArea = (detectObject[2]) * (detectObject[3])
            groundTruthObjectArea = (groundTruthObject[2]) * (groundTruthObject[3])
            # calculate IOU
            objectIOU = intersectionRectangleArea / float(
                detectObjectArea + groundTruthObjectArea - intersectionRectangleArea
            )

            if objectIOU > bigestIOUOfAllGroundTruthObjects:
                bigestIOUOfAllGroundTruthObjects = objectIOU
        if bigestIOUOfAllGroundTruthObjects >= minimumIOU:
            properlyDetectedObjects = properlyDetectedObjects + 1
        objectsIOU.append(bigestIOUOfAllGroundTruthObjects)
        cumulativeIOU = cumulativeIOU + bigestIOUOfAllGroundTruthObjects
    return [cumulativeIOU, properlyDetectedObjects, objectsIOU]
