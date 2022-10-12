from tkinter import *

cameraDistance = 10


window = Tk()
window.title("Test")
window.resizable(False, False)

canvas = Canvas(window, bg="#000000", height=800, width=1000)
canvas.pack()

window.update()

window_height = window.winfo_height()
window_width = window.winfo_width()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

canvas.create_oval(window_width/2 - 10, window_height/2 - 10, window_width/2 + 10, window_height/2 + 10, fill="#FFFFFF")

window.mainloop()