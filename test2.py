from casioplot import *  # this is the calculator's graphics library

points = [
    (-5, -5, 5),
    (5, -5, 5),
    (5, 5, 5),
    (-5, 5, 5),
    (-5, -5, 15),
    (5, -5, 15),
    (5, 5, 15),
    (-5, 5, 15)
]  # simple square corners coordinates


def threeDToTwoD(point, cam):
    f = point[2] - cam[2]
    x = (point[0] - cam[0]) * (f / point[2]) + cam[0]
    y = (point[1] - cam[1]) * (f / point[2]) + cam[1]
    return (round(x), round(y))  # the rounding is because I need integer coordinates for setting the pixel


cam = [0, 0, 0]
while True:
    clear_screen()
    for point in points:
        x, y = threeDToTwoD(point, cam)
        set_pixel(191 + x, 96 - y, (0, 0, 0))
    show_screen()
    cam[2] -= 1  # to move towards the points