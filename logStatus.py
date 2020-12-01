import os

def showCompress(imageFile, outputPath, time):
    sizeFileInput = os.path.getsize(imageFile)
    sizeFileOutput = os.path.getsize(outputPath)
    # performance = ((sizeFileInput/sizeFileOutput) - 1)*100
    compressionRatio = sizeFileOutput/sizeFileInput

    # return nameAlogthim + " Compress: \n" + "   Input File: " + imageFile + "\n   Output File: " + outputPath + "\n   Compress ratio: " + str(compressionRatio)
    
    return  "\n   Output File: "+ outputPath + "\n   ratio: " + str(int(compressionRatio*100)) +"% \n" + "Encode time: "+ str(round(time,3))
def showDecompress(outputPath, fileToSave,  time):
    return  "\n   Output File: " + fileToSave +"\n" + "Decode time: "+ str(round(time,3))
