from tkinter import *
import math
import numpy


def ax_change(value):
    global ax, last_ax_value
    ax += 0.01*(int(value) - last_ax_value)
    last_ax_value = int(value)


def ay_change(value):
    global ay, last_ay_value
    ay += 0.01*(int(value) - last_ay_value)
    last_ay_value = int(value)


def get_position(x, y, z):
    angle = numpy.arctan2(y, x)
    # print(numpy.rad2deg(angle), y, x)
    r = math.sqrt(pow(x, 2)+pow(y, 2))
    # print(r)
    xt, yt = transform_coordinates(angle, r, z)
    return xt, yt


def transform_coordinates(angle, r, h):
    z = get_depth(angle, r, h)
    global d
    global ax
    global ay
    x = (d/(d-z)) * r * math.cos(ax + angle)
    y = (d/(d-z)) * (r * math.sin(ay) * math.sin(ax + angle) + (h * math.cos(ay)))
    return x, y


def get_depth(angle, r, h):
    global ax
    global ay
    c = math.cos(ay)
    number = math.cos(ay) * r * math.sin(ax + angle)
    number2 = math.sin(ay) * h
    depth = number - number2
    return depth


def draw_cube():
    global ax, ay
    # ax += 0.01
    # ay += 0.01
    canvas.delete("all")
    vertexes = [(0, 0) for i in range(0, 8)]
    vertexes[0] = draw_point(1, 1, 1)
    vertexes[1] = draw_point(1, -1, 1)
    vertexes[2] = draw_point(-1, -1, 1)
    vertexes[3] = draw_point(-1, 1, 1)
    vertexes[4] = draw_point(1, 1, -1)
    vertexes[5] = draw_point(1, -1, -1)
    vertexes[6] = draw_point(-1, -1, -1)
    vertexes[7] = draw_point(-1, 1, -1)

    draw_line(vertexes[0][0], vertexes[0][1], vertexes[1][0], vertexes[1][1])
    draw_line(vertexes[1][0], vertexes[1][1], vertexes[2][0], vertexes[2][1])
    draw_line(vertexes[2][0], vertexes[2][1], vertexes[3][0], vertexes[3][1])
    draw_line(vertexes[3][0], vertexes[3][1], vertexes[0][0], vertexes[0][1])

    draw_line(vertexes[0][0], vertexes[0][1], vertexes[4][0], vertexes[4][1])
    draw_line(vertexes[1][0], vertexes[1][1], vertexes[5][0], vertexes[5][1])
    draw_line(vertexes[2][0], vertexes[2][1], vertexes[6][0], vertexes[6][1])
    draw_line(vertexes[3][0], vertexes[3][1], vertexes[7][0], vertexes[7][1])

    draw_line(vertexes[4][0], vertexes[4][1], vertexes[5][0], vertexes[5][1])
    draw_line(vertexes[5][0], vertexes[5][1], vertexes[6][0], vertexes[6][1])
    draw_line(vertexes[6][0], vertexes[6][1], vertexes[7][0], vertexes[7][1])
    draw_line(vertexes[7][0], vertexes[7][1], vertexes[4][0], vertexes[4][1])

    draw_side(vertexes[1], vertexes[2], vertexes[6], vertexes[5], "blue")
    draw_side(vertexes[0], vertexes[1], vertexes[2], vertexes[3], "yellow")
    draw_side(vertexes[0], vertexes[1], vertexes[5], vertexes[4], "red")
    draw_side(vertexes[4], vertexes[5], vertexes[6], vertexes[7], "white")
    draw_side(vertexes[2], vertexes[3], vertexes[7], vertexes[6], "orange")
    draw_side(vertexes[3], vertexes[0], vertexes[4], vertexes[7], "green")
    # if ay > -10:
    window.after(60, draw_cube)


def draw_point(x, y, z):
    point_size = 10
    pos_x, pos_y = get_position(x, y, z)
    pos_x = window_width/2 + pos_x*100
    pos_y = window_height/2 + pos_y*100
    canvas.create_oval(pos_x, pos_y, pos_x+point_size, pos_y+point_size, fill="#FFFFFF")
    return pos_x + point_size/2, pos_y + point_size/2


def draw_line(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, fill="#FFFFFF", width=5)


def draw_side(v1, v2, v3, v4, color):
    canvas.create_polygon(v1[0], v1[1], v2[0], v2[1], v3[0], v3[1], v4[0], v4[1], fill=color)


window = Tk()
window.resizable(False, False)
window.title("Rotating Cube")

label_x = Label(text="X", font=("Courier", 20), fg='#73B5FA', justify=CENTER)
label_x.grid(column=0, row=0)

label_y = Label(text="Y", font=("Courier", 20), fg='#90ee90', justify=RIGHT)
label_y.grid(column=1, row=0)

scale_x = Scale(from_=-400, to=400, length=300, troughcolor='#73B5FA', command=ax_change)
scale_x.grid(column=0, row=1)

scale_y = Scale(from_=-400, to=400, length=300, troughcolor='#90ee90',command=ay_change)
scale_y.grid(column=1, row=1)

canvas = Canvas(window, bg="#333333", height=500, width=800)
canvas.grid(column=2, row=1)


window.update()

window_height = window.winfo_height()
window_width = window.winfo_width()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x_temp = int((screen_width/2)-(window_width/2))
y_temp = int((screen_height/2)-(window_height/2))
#print(window_width, window_height, x, y, screen_width, screen_height)
window.geometry(f"{window_width}x{window_height}+{x_temp}+{y_temp}")

# pseudo camera (0, 10, 0)
last_ax_value = 0
last_ay_value = 0
ax = 0
ay = 0
d = 7
x = 0
y = 0

draw_cube()

window.mainloop()