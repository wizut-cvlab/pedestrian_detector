import cv2


def drawBoxes(image, boxes, color=(0, 255, 0), border=2):
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, border)
