# Pedestrian detector in thermal vision
Detect pedestrians in infrared by Haar Features Cascades. As a ground truth we use tracking manual marked subjects.

## Runing scripts
Dependencies:
```
pip install opencv-python
```

All configurable variables contain `./config.py` file.

Runing:
```
py .\run.py
```

Every time, when:  
-new sequence(folder) is loading,  
-tracker lost object,  
-`space` key was pressed,  
Starts window for select objects for trucking. You need to mark object for frucking using your mouse, then press `space`, to confirm selection. After that you can select another object (pressing `space` one more time), or configm all selected objects by pressing `return`/`enter`.

In real time you can see frame/image, with:  
-green border box - tracked elements,  
-blue border box - detected objects.

## Images dataset
Inside folder `./images/` we assume exist several folders for different images sequences.

All image datasets is located into `images.7z` archive.

## Results
The scripts for each sequences (folders in `./images/`) save a `.txt` file inside `./results/` folder.
Moreover, during computing display results in console.

Results format is:
```
1 1 0 0.546903
```
It means, for specific frame/image (in `.txt` file there is also image name/number):  
-first number describes how many object was tracked (ground truth)  
-second number describes how many object was properly detected  
-third number describes wrong detections  
-last number shows mean IOU for each detected objects on frame,

The Proper detected is, when IOU for detect and ground truth is equal or more than `MINIMUM_IOU` setting in `./config.py`.

## Inside scirpts

### `scripts/addPedestriansToTrack.py`
Function `addPedestriansToTrack` allow to mark multiply object for tracking.

### `scripts/calculateIOU.py`
Function `calculateIOU` calculateIOU for all detection, and count how many detections was correct.

### `scripts/detectPedestrianOnImage.py`
Function `detectPedestrianOnImage` set tracking objects, detect pedestrians and returns IOU between them.

### `scripts/drawBoxes.py`
Function `drawBoxes` draw detect/tracking box on image/frame.

### `scripts/forEachImage.py`
Function `forEachImage` explore `./image/` folder and each subfolder, and on every image runs passed function and collect results.

### `scripts/saveResults.py`
Function `saveResults` save computing results for each subfolder inside `./image/` to given file in `./results` folder.
