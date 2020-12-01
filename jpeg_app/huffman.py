import dahuffman
import numpy
import zipfile
import os


def compress(text, outputPath):

    codec = dahuffman.HuffmanCodec.from_data(text)
    codec.save(path="./table.hm")
    encode = codec.encode(text)
    outFile = open("./code.bin", "wb")
    outFile.write(bytes(encode))
    outFile.close()


    zipf = zipfile.ZipFile(outputPath, 'w', zipfile.ZIP_DEFLATED)
    zipf.write("./table.hm")
    zipf.write("./code.bin")
    zipf.close()
    os.remove("./table.hm")
    os.remove("./code.bin")
    return outputPath


def decompress(filePath):
    with zipfile.ZipFile(filePath, 'r') as zip_file:
        zip_file.extractall("huffman_temp_zip")
    codec = dahuffman.HuffmanCodec.load("huffman_temp_zip\\table.hm")
    with open("huffman_temp_zip\\code.bin", 'rb') as f:
        a = bytes()
        byte = f.read(1)
        while(byte):
            a += byte
            byte = f.read(1)
    import shutil
    shutil.rmtree("huffman_temp_zip")
    return codec.decode(a)


if __name__ == "__main__":
    compress([1, 2, 3, 4, 5, 6, 7], "")
    decompress("./data.jc")
