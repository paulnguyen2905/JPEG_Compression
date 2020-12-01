from jpeg_app import GUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    h = GUI.GUI(root)
    h.setWindow()
    h.drawUI()
    root.mainloop()