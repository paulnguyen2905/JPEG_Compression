import cv2
import numpy as np
import os
from . import zigzag
from . import QuantizationTables
from . import RunLengthCoding as RLE
from . import logStatus
import time
from . import huffman

class JPEG:
    def __init__(self):
        self.NUM_SIZE_BLOCK = 8

    def rgb2ycbcr(self, im):
        xform = np.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
        ycbcr = im.dot(xform.T)
        ycbcr[:,:,[1,2]] += 128
        return np.uint8(ycbcr)

    def ycbcr2rgb(self, im):
        xform = np.array([[1, 0, 1.402], [1, -0.34414, -.71414], [1, 1.772, 0]])
        rgb = im.astype(np.float)
        rgb[:,:,[1,2]] -= 128
        rgb = rgb.dot(xform.T)
        np.putmask(rgb, rgb > 255, 255)
        np.putmask(rgb, rgb < 0, 0)
        return np.uint8(rgb)

    def initEncode(self, imageFile):
        self.img = cv2.imread(imageFile)
        self.img = self.rgb2ycbcr(self.img)

        self.heightOrigin, self.widthOrigin = self.img.shape[:2]

        re = self.heightOrigin % self.NUM_SIZE_BLOCK 
        if (re == 0):
            self.heightNew = self.heightOrigin
        else:
            self.heightNew = (int(self.heightOrigin/self.NUM_SIZE_BLOCK) + 1)*self.NUM_SIZE_BLOCK

        if (self.widthOrigin % self.NUM_SIZE_BLOCK == 0):
            self.widthNew = self.widthOrigin
        else:
            self.widthNew = (int(self.widthOrigin/self.NUM_SIZE_BLOCK) + 1)*self.NUM_SIZE_BLOCK

    def enCodeAChannel(self, ChannelColor, isYChannel):
        #init
        newImage = np.zeros((self.heightNew, self.widthNew), np.float32)
        newImage[:self.heightOrigin, :self.widthOrigin] = ChannelColor
    
        # Q = np.zeros((self.heightNew, self.widthNew), np.int32)

        DC = []
        AC = []
        quantizationTable = []
        if isYChannel:
            quantizationTable = self.luminaceTable
        else:
            quantizationTable = self.chrominaceTable
        DC_behind_coefficient = 0

        for row in range(self.blocksV):
            for col in range(self.blocksH):
                currentBlock = cv2.dct(newImage[row*self.NUM_SIZE_BLOCK:(row + 1)*self.NUM_SIZE_BLOCK, col*self.NUM_SIZE_BLOCK:(col + 1)*self.NUM_SIZE_BLOCK])
                
                divice = currentBlock/quantizationTable
                divice = divice.astype(int)

                # Trans[row*self.NUM_SIZE_BLOCK: (row + 1)*self.NUM_SIZE_BLOCK, col*self.NUM_SIZE_BLOCK: (col + 1)*self.NUM_SIZE_BLOCK] = currentBlock
                # Q[row*self.NUM_SIZE_BLOCK: (row + 1)*self.NUM_SIZE_BLOCK, col*self.NUM_SIZE_BLOCK: (col + 1)*self.NUM_SIZE_BLOCK] = divice

                DC_coefficient = divice[0, 0]
                lenDC = len(DC)
                if (lenDC == 0):
                    DC.append(DC_coefficient)
                else:
                    DC.append(DC_behind_coefficient - DC_coefficient)

                DC_behind_coefficient = DC_coefficient

                AC += zigzag.ZigZag().getArrayZigZag(divice)
        AC_RLE = RLE.encodeRunLengthEncoding(AC)

        lenDC = len(DC)
        lenAC = len(AC_RLE)
        return [lenDC, lenAC] + DC + AC_RLE

    def encodeJPEG(self, imageFile, quality=1):
        now = time.time()
        self.initEncode(imageFile)
        filename, fileExtension = os.path.splitext(imageFile)

        # Trans = np.zeros((heightNew, widthNew), np.float32)
    
        self.chrominaceTable = QuantizationTables.TableLChrominaces[quality]
        self.luminaceTable = QuantizationTables.TableLuminances[quality]
        
        self.blocksV = int(self.heightNew/self.NUM_SIZE_BLOCK)
        self.blocksH = int(self.widthNew/self.NUM_SIZE_BLOCK)

        channels = cv2.split(self.img)
        result = []
        for i in range(3): #Blue, green, red
            if i!=0:
                result.append(self.enCodeAChannel(channels[i],False))
            else :
                result.append(self.enCodeAChannel(channels[i],True))
        
        quantizationList = []
        for i in self.chrominaceTable:
            for j in i:
                quantizationList.append(j)
        for i in self.luminaceTable:
            for j in i:
                quantizationList.append(j)

        head = [self.heightNew, self.widthNew, self.heightOrigin, self.widthOrigin] + quantizationList

        listToEncode = head + result[0] + result[1] + result[2]
        outputPath = huffman.compress(listToEncode, outputPath=filename+ ".bin")

        log = logStatus.showCompress(imageFile, outputPath, time.time()-now)
        return outputPath, log
        
    def getTableFromList(self, dataList):
        arr = []
        for i in range(self.NUM_SIZE_BLOCK):
            arr.append(dataList[i*self.NUM_SIZE_BLOCK:(i+1)*self.NUM_SIZE_BLOCK])
        return arr

    def initDecode(self, arrEncode):
        self.heightNew_decode = arrEncode[0]
        self.widthNew_decode = arrEncode[1]
        self.heightOrigin_decode = arrEncode[2]
        self.widthOrigin_decode = arrEncode[3]

        arrEncode = arrEncode[4:]
        quantizationList_decode = arrEncode[:64]
        self.chrominaceTable_decode = self.getTableFromList(quantizationList_decode)
        arrEncode = arrEncode[64:]
        quantizationList_decode = arrEncode[:64]
        self.luminaceTable_decode = self.getTableFromList(quantizationList_decode)
        arrEncode = arrEncode[64:]

        lenDC, lenAC = arrEncode[0], arrEncode[1]
        blueNew = arrEncode[: 2 + lenDC + lenAC]
        arrEncode = arrEncode[2 + lenDC + lenAC:]

        lenDC, lenAC = arrEncode[0], arrEncode[1]
        greenNew = arrEncode[: 2 + lenDC + lenAC]
        arrEncode = arrEncode[2 + lenDC + lenAC:]

        redNew = arrEncode

        self.blocksV_decode = int(self.heightNew_decode/self.NUM_SIZE_BLOCK)
        self.blocksH_decode = int(self.widthNew_decode/self.NUM_SIZE_BLOCK)

        self.Channel_decode = [blueNew, greenNew, redNew]

    def decodeChannel(self, channel_decode, isYChannel):
        lenDC = channel_decode[0]

        DC = channel_decode[2 : 2 + lenDC]
        AC = RLE.decodeRunLengthCoding(channel_decode[2 + lenDC:])

        newImage = np.zeros((self.heightNew_decode, self.widthNew_decode), np.float32)
        quantizationTable_decode = []
        if isYChannel:
            quantizationTable_decode = self.luminaceTable_decode
        else:
            quantizationTable_decode = self.chrominaceTable_decode
        flag = 0
        DC_coefficient_current = DC[flag]
        i = 0
        for row in range(self.blocksV_decode):
            for col in range(self.blocksH_decode):
                #-------------------
                currentBlock = zigzag.ZigZag().getUnCovertZigZag(AC[i:i + 63])
                i += 63
                if (flag == 0):
                    currentBlock[0,0] = DC[flag]
                    DC_coefficient_current = DC[flag]
                else:
                    DC_coefficient_current = DC_coefficient_current - DC[flag]
                    currentBlock[0,0] = DC_coefficient_current
                flag += 1
                #-------------------
                currentBlock = currentBlock*quantizationTable_decode
                
                newImage[row*self.NUM_SIZE_BLOCK:(row + 1)*self.NUM_SIZE_BLOCK, 
                        col*self.NUM_SIZE_BLOCK:(col + 1)*self.NUM_SIZE_BLOCK] = cv2.idct(currentBlock.astype(np.float32))               
                
        return newImage

    def decode(self, outputPath, fileToSave):
        now = time.time()
        arrEncode = huffman.decompress(outputPath)

        self.initDecode(arrEncode)
       
        decode = []
        for i in range(3):
            if i!=0:
                decode.append(self.decodeChannel(self.Channel_decode[i], False)[:self.heightOrigin_decode,:self.widthOrigin_decode])
            else:
                decode.append(self.decodeChannel(self.Channel_decode[i], True)[:self.heightOrigin_decode,:self.widthOrigin_decode])

        imgFinal = self.ycbcr2rgb(cv2.merge([decode[0], decode[1], decode[2]]))
        cv2.imwrite(fileToSave, imgFinal)

        log = logStatus.showDecompress(outputPath, fileToSave, time.time()-now)
        return log

