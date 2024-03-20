# CubeSolver

CubeSolver is a program that solves the Rubik's Cube using the LBL (Layer-by-Layer) method, mimicking the way humans typically solve it. To launch the program, run `RC.py`.

![Rubik's Cube](https://github.com/Mikosztyla/CubeSolver/assets/115586050/2a65a7d7-43f7-412e-8de9-523fb8754481)

The program utilizes PyGame to project the cube in 3D with perspective, achieved through low-level matrix multiplication.

Controls:
- Use `Q` and `W` to rotate the cube around the X-axis.
- Use `A` and `S` to rotate the cube around the Y-axis.
- Use `Z` and `X` to rotate the cube around the Z-axis.

![Controls](https://github.com/Mikosztyla/CubeSolver/assets/115586050/8fb4b5d9-1b50-4124-aaae-e3ea250de042)

Additionally, you can use buttons on the left to rotate specific sides of the cube, following the Rubik's Cube notation. Refer to the notation guide [here](https://ruwix.com/the-rubiks-cube/notation/).

After using `solve` and `scramble` buttons, the console will display the moves executed by the algorithm.

Give it a try and see if you can solve it by yourself!
