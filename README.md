# Mango (Amanda Zheng [P10] and George Zhou [P04])
Note: MDL files are placed in the `mdl` directory for removal of clutter inside the repository.
## Modified MDL commands
### Vary
There are a total of 7 types of vary commands you can use when animating objects in a gif. This is the general format for the command, in general, for vary types:
```
vary <knob_name> <start_frame> <end_frame> <start_val> <end_val> <vary_type>
```
#### linear
#### accelerate
#### decelerate
#### pause
#### cosine
#### sine
#### bouncing
two optional inputs for bounce command: vary varname frame_begin frame_end 0 1 bouncing <num_bounces> <decay>
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
