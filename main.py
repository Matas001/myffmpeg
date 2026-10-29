import ffmpeg
import tkinter as tk
import os
import io
from tkinter.filedialog import askopenfile, asksaveasfile, Open
from PIL import Image, ImageTk


root = tk.Tk()


width = 500
height = 300
root.minsize(width,height)
root.maxsize(width,height)
root.title("FFMPEG")
root.resizable(0,0)

filename = None
file = None
videothumbnail = None
fileinput = None

def IsVideo(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension in [".mp4", ".avi", ".mov", ".mkv", ".webm", ".wmv", ".flv", ".mpeg", ".mpg", ".m4v"]




def SelectFile():
    global filename
    global fileinput
    global file
    global videothumbnail
    file = askopenfile()
    if file:
        fileinput = ffmpeg.input(file.name)
        filename = file.name
        videothumbnail = None

        if IsVideo(filename):
            try:
                videothumbnail, _ = ffmpeg.input(filename, ss=0).output("pipe:", vframes=1, format="image2pipe", vcodec="png").run(capture_stdout=True, capture_stderr=True)
            except ffmpeg.Error as e:
                print(e.stderr.decode("utf-8", errors="replace"))

        update()

def AskToSave():
    dir = asksaveasfile()
    print(dir)
    Open(dir)
    return dir

def SaveToGif():
    fileinput.output(str(AskToSave())+"\image.gif",vf="split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse").run()


frame = tk.Frame(root,width=300,height=300)
frame.pack_propagate(False)
frame.pack(side=tk.LEFT)

photoframe = tk.Frame(root,width=200,height=300)
photoframe.pack_propagate(False)

photoframe.pack(side=tk.RIGHT)



photolabel = tk.Label(photoframe)
photolabel.pack(fill="both", expand=True)



gui = {
    "SelectFile":tk.Button(frame, text="Select File", command=SelectFile),
    "Label":tk.Label(frame,text="nothing"),
    "Save":tk.Button(frame, text="Save To .gif", command=SaveToGif),
}



def update():
    global preview
    if filename:
        gui["Label"].config(text="Selected File: "+os.path.basename(filename))
        gui["Save"].config(state=tk.NORMAL)
    else:
        gui["Label"].config(text="Selected File: None")
        gui["Save"].config(state=tk.DISABLED)
    if file:
        try:
            if IsVideo(filename):
                image = Image.open(io.BytesIO(videothumbnail))
            else:
                image = Image.open(filename)

            image.thumbnail((200, 300))
            preview = ImageTk.PhotoImage(image)
            photolabel.config(image=preview)
            photolabel.image = preview
        except Exception as e:
            print(e)

for x in gui:
    gui[x].pack(anchor="nw",fill="x")


update()
root.mainloop()