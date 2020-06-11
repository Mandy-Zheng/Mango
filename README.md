# Mango (Amanda Zheng [P10] and George Zhou [P04])
## Modifying MDL commands
### Knob
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
Provided an '.obj' file, it will place that object in the image
'''
mesh [<constant>] :<filename> [<coordinate_system>]
'''
Uses a function in 'mdl.py' which parses the '.obj' file.
All '.obj' files **must** be placed in the 'obj' directory.

## New MDL commands
### Cylinder Shape (x, y, z, radius, height)
**cylinder based on center of top circle**
### Cone Shape (x, y, z, radius, height)
**cone based on center of circle**

**mdl files should be stored in mdl directory**
