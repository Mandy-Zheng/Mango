# Team Mango (Amanda Zheng [P10] and George Zhou [P04])
Note: MDL files are placed in the `mdl` directory for removal of clutter inside the repository.
## Modified MDL commands
### Vary
There are a total of 7 types of vary commands you can use when animating objects in a gif. This is the general syntax for the command, in general, for vary types:
```
vary <knob_name> <start_frame> <end_frame> <start_val> <end_val> <vary_type>
```
#### linear
The object will go from one value to another in linear fashion with constant velocity
#### accelerate
The object will go from the beginning value to the ending one in quadratic function. There will be constant acceleration, starting at 0 velocity, and the equations of physics was used to figure out the displacement at every frame.
#### decelerate
Similar to ``accelerate``, but the object will end at 0 velocity, instead of starting. 
#### pause
This type combines the accelerate and decelerate into one action. The object first decelerates to the midpoint between the start and end value. At the midpoint, the instantaneous velocity is 0, and then it accelerates to the end value.
#### cosine
This is one of the two circular motions an object can do. The object will follow the cosine function from `0` to `<end_frame> - <start_frame>` where the function has an amplitude of `0.5 * (<end_val> - <start_val>)` and a cycle of `2 * (<end_frame> - <start_frame>)`. Note that the end points have 0 velocity while the midpoint has the highest velocity.
#### sine
This is the other of the two circular motions an object can do. The object will follow the sine function from `0` to `<end_frame> - <start_frame>` where the function has an amplitude of `(<end_val> - <start_val>)` and a cycle of `2 * (<end_frame> - <start_frame>)`. Note that the end points have highest velocity while the midpoint has the 0 velocity. In addition, the sine type will go from `<start_val>` to `<end_val>` with reaching the `end_val` at the halfway point. This is because there is no elegant way to make this sine function mathematically aesthetically pleasing.
#### bouncing
The bouncing function oscillates between accelerate and decelerate, starting at accelerate and ending at accelerate. The ball will move back and forth between the `<start_val>` and `<end_val>`, but it will never reach the `<start_val>` ever again. Because of the nature of this vary type, the ``bouncing`` type will have the following syntax:
```
vary <knob_name> <start_frame> <end_frame> <start_val> <end_val> bouncing [<num_bounces>] [<decay_rate>]
```
These two optional inputs make this type very changeable to your needs. If you don't provide the `<decay_rate>`, it will automatically be set to `0.5`. If you don't provide both the `<decay_rate>` and `<num_bounces>`, then the `<num_bounces>` will automatically be set to `1`. The `<decay_rate>` represents how much the height of the object decays on the next bounce. The `<num_bounces>` represents how many time the ball bounces. Note that when the object finally comes to a stop, that stopping point does not count as a bounce.

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
### Cone
Creates a right, vertical cone in the image.
```
cone [<constant>] <x> <y> <z> <radius> <height> [<coordinate_system>]
```
The coordinates (x, y, z) is the center of the circular base at the bottom of the cone and the cone will be created from bottom to top.
