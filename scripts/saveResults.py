def saveResults(folderName, detectionResults, resultsFolder=".\\"):
    with open(resultsFolder + folderName + ".txt", "w") as file:
        for result in detectionResults:
            file.write(
                "%s %d %d %d %f\n"
                % (
                    result["file"],
                    result["results"]["trackingObjects"],
                    result["results"]["properlyDetectedObjects"],
                    result["results"]["wrongDetections"],
                    result["results"]["meanIOU"],
                )
            )
        file.close()
        print("Saved results for " + folderName)
