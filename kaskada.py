import cv2
import os
import glob
import json

rootdir = "C:\\Users\\asmolinski\\Desktop\\maruda\\"
imgfolder = "test4\\kal\\z\\"

cascade = cv2.CascadeClassifier(rootdir + "maruda.xml")


for filename in glob.glob(os.path.join(rootdir + imgfolder, "*.jpg")):

    print(filename)

    img = cv2.imread(filename, 1)
    if img is None:
        continue

    picture_data = []
    people = cascade.detectMultiScale(img, 1.02, 3)  # 4,0, (110, 110))
    print("Number of sihouettes detected: {}".format(len(people)))
    for (x, y, w, h) in people:
        picture_data.append(
            {
                "bottomright": {"x": int(x + w), "y": int(y + h)},
                "topleft": {"x": int(x), "y": int(y)},
            }
        )

    with open(filename.replace(".jpg", ".json"), "w") as outfile:
        json.dump(picture_data, outfile)
