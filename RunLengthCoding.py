def encodeRunLengthEncoding(input):
    output = []
    n = len(input)
    i = 0
    while i < n:
        if input[i] == 0:
            count = 1
            while (i < n - 1 and input[i] == input[i+1]):
                count+=1
                i+=1
            output.append(count)
            output.append(input[i])
        else:
            output.append(input[i])
        i+=1
    return output

def decodeRunLengthCoding(inputArr):
    i = 0
    n = len(inputArr)
    output = []
    while i < n:
        if i <= n - 2:
            if (inputArr[i] != 0 and inputArr[i+1] == 0):
                for _ in range(inputArr[i]):
                    output.append(inputArr[i+1])
                i += 2
            else:
                output.append(inputArr[i])
                i+=1
        else:
            output.append(inputArr[i])
            i+=1
    return output

