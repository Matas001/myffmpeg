import tkinter as tk
import tempfile
import os


root = tk.Tk()


width = 500
height = 300
root.minsize(width,height)
root.maxsize(width,height)
root.title("FFMPEG")
root.resizable(0,0)










mainframe = tk.Frame(root,width=300,height=300)
mainframe.pack_propagate(False)
mainframe.pack(side=tk.LEFT)

photoframe = tk.Frame(root,width=200,height=300)
photoframe.pack_propagate(False)
photoframe.pack(side=tk.RIGHT)

preview = tk.Label(photoframe)
preview.pack(fill="both",expand=True)




#variables

file = None



import ffmpeg
from tkinter import filedialog
#functions




def IsVideo(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension in [".mp4", ".avi", ".mov", ".mkv", ".webm", ".wmv", ".flv", ".mpeg", ".mpg", ".m4v"]


def GetFileName(file):
    return os.path.basename(file).split(".")[0]

def GetFileExtenstion(file):
    return os.path.basename(file).split(".")[1]

def GetFileBaseName(file):
    return os.path.basename(file)


def SelectFile():
    global file

    file = filedialog.askopenfile()
    update()


def ToGif():
    dir = filedialog.asksaveasfile(filetypes=(("gif","*.gif"),("any","*.*")),initialfile=GetFileName(file.name)+".gif")
    if dir:
        ffmpeg.input(file.name).output(dir.name,vf="split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse").run(overwrite_output=True)  

def ToPng():
    dir = filedialog.asksaveasfile(filetypes=(("png","*.png"),("any","*.*")),initialfile=GetFileName(file.name)+".png")
    if dir:
        ffmpeg.input(file.name).output(dir.name).run(overwrite_output=True)

def ToMp4():
    dir = filedialog.asksaveasfile(filetypes=(("mp4","*.mp4"),("any","*.*")),initialfile=GetFileName(file.name)+".mp4")
    if dir:
        ffmpeg.input(file.name).output(dir.name).run(overwrite_output=True)

def ToWebp():
    dir = filedialog.asksaveasfile(filetypes=(("webp","*.webp"),("any","*.*")),initialfile=GetFileName(file.name)+".webp")
    if dir:
        ffmpeg.input(file.name).output(dir.name).run(overwrite_output=True)

def ToAny():
    dir = filedialog.asksaveasfile(filetypes=(("any","*.*"),("webp","*.webp"),("mp4","*.mp4"),("png","*.png"),("gif","*.gif")),initialfile=GetFileName(file.name))
    if dir:
        ffmpeg.input(file.name).output(dir.name).run(overwrite_output=True)


from PIL import Image, ImageTk

def update():
    state = "disabled"


    if file:
        state = "normal"
        gui["Label"].config(text="Selected File: "+GetFileBaseName(file.name))

        
        if IsVideo(file.name):
            tempdir = os.path.join(tempfile.gettempdir(), "FFMPEG-thumbnail.png")
            try:
                ffmpeg.input(file.name).output(tempdir).run(overwrite_output=True)
            except:
                print("FFMPEG Failed") # happens even if it succeeds for some reason
            image = Image.open(tempdir)
        else:
            image = Image.open(file.name)

        
        image.thumbnail((200,300))
        photoimage = ImageTk.PhotoImage(image)
        preview.config(image=photoimage)
        preview.image = photoimage

    
    for x in gui:
        if x != "SelectFile" and x != "Label":
            gui[x].config(state=state)







gui = {
    "SelectFile":tk.Button(mainframe, text="Select File", command=SelectFile),
    "Label":tk.Label(mainframe,text="Selected File: None"),
    "Gif":tk.Button(mainframe, text="Save To .gif", command=ToGif),
    "Png":tk.Button(mainframe, text="Save To .png", command=ToPng),
    "Mp4":tk.Button(mainframe, text="Save To .mp4", command=ToMp4),
    "Webp":tk.Button(mainframe, text="Save To .webp", command=ToWebp),
    "Any":tk.Button(mainframe, text="Save To .*", command=ToAny),
}

for x in gui:
    gui[x].pack(anchor="nw",fill="x")


# watermark


import webbrowser

def OpenGithub():
    webbrowser.open("https://github.com/Matas001")


watermark = tk.Button(root,text="Made by: Matas001",relief="flat",command=OpenGithub)
watermark.place(relx=0, rely=1,anchor="sw")

update()
root.mainloop()