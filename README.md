# Mango (Amanda Zheng [P10] and George Zhou [P04])
## Modified MDL commands
### Vary
    - Adding 6 nonlinear animations (in addition to linear)
        - bouncing
        - sin
        - cos
        - accelerate
        - decelerate
        - pause
        **place vary type at the end of vary type**
        **two optional inputs for bounce command: vary varname frame_begin frame_end 0 1 bouncing <num_bounces> <decay>**
### Mesh
Provided an `.obj` file, it will place that mesh object in the image.
```
mesh [<constant>] :<filename> [<coordinate_system>]
```
Uses a function in `mdl.py` called `objParse()` which parses the `.obj` file. All `.obj` files **MUST** be placed in the `obj` directory in order for the file to be actually parced.

## New MDL commands
### Cylinder
Creates a right, vertical cylinder in the image.
```
cylinder [<constant>] <x> <y> <z> <radius> <height> [<coordinate_system>]
```
The coordinates (x, y, z) is the center of the circular base at the top of the cyclinder and the cylinder will be created from top to down.
### Cone Shape (x, y, z, radius, height)
Creates a right, vertical cone in the image.
```
cone [<constant>] <x> <y> <z> <radius> <height> [<coordinate_system>]
```
The coordinates (x, y, z) is the center of the circular base at the bottom of the cone and the cone will be created from bottom to top.

**mdl files should be stored in mdl directory**
