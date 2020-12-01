import numpy as np

class ZigZag:
    def __init__(self, maxx = 7, minn = 0):
        self.result = []
        self.MAXX = maxx
        self.MINN = minn
        
    def getArrayZigZag(self, arrInput):
        x = 0
        y = 1
        xIncrease = True
        yIncrease = False

        self.result = []
        self.result.append(arrInput[x][y])
        while (True):
            if(xIncrease):
                x += 1
            else:
                x -= 1
            
            if(yIncrease):
                y += 1
            else:
                y -= 1
            self.result.append(arrInput[x][y])

            if(x == self.MAXX and y == self.MAXX):
                break
            
            change = False
            if (x == self.MAXX and y == self.MINN):
                y = self.MINN + 1
                xIncrease = False
                yIncrease = True
                change = True
            elif (y == self.MINN and not(yIncrease)):
                x += 1
                xIncrease = False
                yIncrease = True
                change = True
            elif (x == self.MINN and not(xIncrease)):
                y += 1
                xIncrease = True
                yIncrease = False
                change = True
            elif (x == self.MAXX and xIncrease):
                y += 1
                xIncrease = False
                yIncrease = True
                change = True
            elif (y == self.MAXX and yIncrease):
                x += 1
                xIncrease = True
                yIncrease = False
                change = True

            if change:
                self.result.append(arrInput[x][y])
                change = False
                if(x == self.MAXX and y == self.MAXX):
                    break

        return self.result

    def getUnCovertZigZag(self, arrInput):
        flag = 0
        arr = np.zeros((self.MAXX + 1, self.MAXX + 1), np.int32)

        x = 0
        y = 1
        xIncrease = True
        yIncrease = False

        arr[x, y] = arrInput[flag]
        flag += 1
        while (True):
            if(xIncrease):
                x += 1
            else:
                x -= 1
                
            if(yIncrease):
                y += 1
            else:
                y -= 1

            arr[x, y] = arrInput[flag]
            flag += 1

            if(x == self.MAXX and y == self.MAXX):
                break
                
            change = False
            if (x == self.MAXX and y == self.MINN):
                y = self.MINN + 1
                xIncrease = False
                yIncrease = True
                change = True
            elif (y == self.MINN and not(yIncrease)):
                x += 1
                xIncrease = False
                yIncrease = True
                change = True
            elif (x == self.MINN and not(xIncrease)):
                y += 1
                xIncrease = True
                yIncrease = False
                change = True
            elif (x == self.MAXX and xIncrease):
                y += 1
                xIncrease = False
                yIncrease = True
                change = True
            elif (y == self.MAXX and yIncrease):
                x += 1
                xIncrease = True
                yIncrease = False
                change = True

            if change:
                arr[x, y] = arrInput[flag]
                flag += 1
                change = False
                if(x == self.MAXX and y == self.MAXX):
                    break
        return arr
        