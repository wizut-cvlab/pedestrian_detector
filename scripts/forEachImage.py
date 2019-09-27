import os
from glob import glob
import config
import cv2


def forEachImage(
    folder,
    imageFunction,
    imageFunctionArgs={},
    folderFunction=None,
    folderFunctionArgs={},
):
    allImagesResults = []
    foldersResults = []
    for subFolder in os.listdir(folder):
        imageFunctionResults = []
        imageResult = {}
        for file in os.listdir(folder + subFolder):
            fileName, fileExtension = os.path.splitext(file)
            if fileExtension.lower() not in config.IMAGE_EXTENTIONS:
                continue
            greyImage = cv2.imread(
                folder + subFolder + "\\" + file, cv2.IMREAD_GRAYSCALE
            )
            if greyImage is None:
                continue
            image = cv2.cvtColor(greyImage, cv2.COLOR_GRAY2RGB)
            imageResult = imageFunction(image, imageResult, **imageFunctionArgs)
            imageFunctionResults.append({"file": fileName, "results": imageResult})
            allImagesResults.append(
                {"file": subFolder + "/" + fileName, "results": imageResult}
            )
        if folderFunction:
            foldersResults.append(
                folderFunction(subFolder, imageFunctionResults, **folderFunctionArgs)
            )
    return [allImagesResults, foldersResults]
