import tkinter as tk
from tkinter import filedialog
import os
from . import JPEG_compress

class GUI:
    def __init__(self, root):
        self.root = root
        self.textColor = "#393e46"
        self.buttonColor = "#393e46"    
        self.xForBtn = 430
        self.xForEntry = 120
        self.xForLabel = 10
        self.font = "Century Gothic"
        self.quality = 95
        self.fileName = ""
        self.log = tk.Label()
    def setWindow(self):
        self.root.title("Jpeg compress")
        width, height = 500, 360            #500, 530
        self.root.geometry("%dx%d"%(width,height))

        #Display infor, title
        tk.Label(self.root, text = "University of Information Technology", font = (self.font, 10), fg = self.textColor).place(x = 131, y = 3)
        tk.Label(self.root, text = "Multimedia Computing-CS232.K23.KHCL", font = (self.font, 10 ), fg = self.textColor).place(x = 119, y = 23)
        tk.Label(self.root, text = "JPEG COMPRESSION", font = (self.font, 16, "bold"), fg = self.textColor).place(x = 146, y = 48)

    def drawUI(self):

        # Display open image
        tk.Label(self.root, text = "File path", font = (self.font, 12, "bold"), fg = self.textColor).place(x = self.xForLabel, y = 105)

        dirEntry = tk.Entry(self.root, textvariable = "",  font = (self.font, 12), width = 32)
        dirEntry.pack()
        dirEntry.insert(0, "")
        dirEntry.place(x = self.xForEntry, y = 105)

        btnOpenFile = tk.Button(self.root, text = "Select File", width = 10, height = 2, bg = self.buttonColor, fg = "#FFFFFF", command=lambda:self.DirFileDialog(dirEntry))
        btnOpenFile.place(x = self.xForEntry, y = 150)

        tk.Label(self.root, text = "JPEG COMPRESSION", font = (self.font, 16, "bold"), fg = self.textColor).place(x = 146, y = 48)
        tk.Label(self.root, text = "#2020", font = (self.font, 8), fg = self.textColor).place(x = 460, y = 511)

        btnLossy = tk.Button(self.root,  text = "Encode", width = 10, height = 2, bg = self.buttonColor, fg = "#FFFFFF", command=lambda:self.actionCompress())
        btnLossy.place(x = self.xForEntry+105, y = 150)

        btnDeLossy = tk.Button(self.root, text = "Decode", width = 10, height = 2, bg = self.buttonColor, fg = "#FFFFFF", command=lambda:self.actionDecompress(".bmp"))
        btnDeLossy.place(x = self.xForEntry+210, y = 150)

        tk.Label(self.root, text = "Quality", font = (self.font, 12, "bold"), fg = self.textColor).place(x = self.xForLabel, y = 215)
        
        tkScale = tk.Scale(self.root, orient=tk.HORIZONTAL,length=290,width=10,sliderlength=10,from_=1,to=4,tickinterval=1, command=self.set_value)
        tkScale.set(2)
        tkScale.place(x = 120, y = 200)
        
        

    def DirFileDialog(self, dirEntry):
        self.fileName = filedialog.askopenfilename(initialdir = "/",title = "Select Picture",filetypes = (("Bitmap Image File","*.BMP")
                                                                ,("JPEG", "*.JPEG;*.JPG;*.JPE"),
                                                                ("PNG", "*.PNG"),
                                                                ("BIN", "*.BIN"),
                                                                ("Numpy array Python", "*.npy"),
                                                                ("All Files","*.*")))
        FileCSV = self.fileName 
        dirEntry.delete(0, tk.END)
        dirEntry.insert(0,FileCSV)          

    def set_value(self, val):      
        self.quality = int(val)-1

    def actionCompress(self):
        
        # try:
        outputPath, log = JPEG_compress.JPEG().encodeJPEG(self.fileName, int(self.quality))
        self.log.after(0,self.log.destroy)
        self.log = tk.Label(self.root, text = log, font = (self.font, 12), fg = self.textColor)
        self.log.place(x = 120, y = 250)

    def actionDecompress(self, typeFile):
        filename, fileExtension = os.path.splitext(self.fileName)

        fileToSave = filename + "_decode" + typeFile
        log = JPEG_compress.JPEG().decode(self.fileName, fileToSave)
        self.log.after(0,self.log.destroy)
        self.log = tk.Label(self.root, text = log, font = (self.font, 12), fg = self.textColor)
        self.log.place(x = 100, y = 250)


if __name__ == "__main__":
    root = tk.Tk()
    h = GUI(root)
    h.setWindow()
    h.drawUI()
    root.mainloop()