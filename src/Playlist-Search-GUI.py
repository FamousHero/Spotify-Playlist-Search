import tkinter as tk
from tkinter.constants import END, INSERT
from client import Client
def GUI():
    client = Client()
    root_window = tk.Tk()
    root_window.title("GUI")
    root_window.columnconfigure(0, weight=1)
    root_window.columnconfigure(1, weight=1)
    root_window.columnconfigure(2, weight=1)

    root_window.rowconfigure(0, weight=1)
    root_window.rowconfigure(1, weight=1)
    root_window.rowconfigure(2, weight=1)
    root_window.rowconfigure(3, weight=1)
    root_window.rowconfigure(4, weight=1)

    leftframe = tk.Frame(root_window, bg="pink", width=200)
    leftframe.grid(row=0,rowspan=5, column=0, sticky="NSEW")
    rightframe = tk.Frame(root_window, bg="pink", width=200)
    rightframe.grid(row=0, rowspan=5, column=2, sticky="NSEW")
    centertop = tk.Frame(root_window, width=400, height=250)
    centertop.grid(row=0, rowspan=2, column=1, sticky="NSEW")
    centerlabel = tk.Label(text="Hello", justify="center", bg="pink", fg="blue", font=("Lucida Calligraphy", "16"))
    centerlabel.grid(row=0, column=1, sticky="NSEW")
    midtop = tk.Frame(root_window, bg="pink", width= 400, height = 100)
    midtop.grid(row=1, column=1, rowspan=2, sticky="NSEW")
    centerbottom = tk.Frame(root_window, bg="pink", height=250)
    centerbottom.grid(row=2, rowspan=3, column=1, sticky="NSEW")
    songname = tk.Entry(root_window, justify="center")
    songname.grid(row=1, column=1, sticky="EW")
    songname.insert(0, "What song would you like to search")
    

    searchbutton =tk.Button(master=root_window, text="Search", command=lambda:display("name", songname.get()))
    searchbutton.grid(row=2, rowspan=2, column=1)

    currentbutton = tk.Button(master=root_window, text="Search current Song", command= lambda:display("current_song"))
    currentbutton.grid(row=3, column=1)
    def display(type, songname=None):
        playlists_to_display=client.search(type, songname)
        centerlabel['text'] = playlists_to_display
        centerlabel['font'] = ("Lucida Calligraphy", "16")

    root_window.mainloop()


if __name__ == "__main__":
    GUI()
