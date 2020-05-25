import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):

    name = ''
    num_frames = 1
    vary=False;

    for command in commands:
        c = command['op']
        args = command['args']
        if c == "vary":
            vary=True;
        elif c == "basename":
            name = args[0]
        elif c == "frames":
            num_frames = int(args[0])
    if name == '':
        print("Warning! No Basename provided. Default Basename: img")
        name = "img"
    if num_frames == 1 and vary:
        print("Compiler Error: Expected more than one frame for Vary command")
        exit()
    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the command['knob'] for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. command['knob'][0] would be the first
  frame, command['knob'][2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from command['knob'][0] to command['knob'][frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [ {} for i in range(num_frames) ]
    for command in commands:
        c = command['op']
        args = command['args']
        if c == "vary":
            if num_frames>1:
                start = int(args[0])
                end = int(args[1])
                value1 = args[2]
                value2 = args[3]
                knob = command ['knob']
                if args[4] == "linear":
                    dx = (value2-value1)/(end-start)
                    while start <= end:
                        frames[start][knob] = value1
                        value1 += dx
                        start += 1
                elif args[4]=="accelerate":
                    dx = (1.0/end) / ((end // 2)+1)
                    if(value2<value1):
                        dx=-1*dx
                    while start <= end:
                        frames[start][knob] = value1
                        start += 1
                        value1 = value1+start*dx
                elif args[4]=="decelerate":
                    dx = (1.0/end) / ((end // 2)+1)
                    if(value2<value1):
                        dx=-1*dx
                    while start <= end:
                        frames[start][knob] = value1
                        start += 1
                        value1 = value1+(num_frames-start)*dx


    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)
    count_frames = 0

    while(count_frames < num_frames):
        print("Creating Frame #"+str(count_frames))
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []

        for command in commands:
            c = command['op']
            args = command['args']
            #print(command)
            knob_value = 1

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'cylinder':
                if command['constants']:
                    reflect = command['constants']
                add_cyl(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if command['knob']:
                    knob_value = frames[count_frames][command['knob']]
                tmp = make_translate(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                if command['knob']:
                    knob_value = frames[count_frames][command['knob']]
                tmp = make_scale(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                if command['knob']:
                    knob_value = frames[count_frames][command['knob']]
                theta = args[1] * (math.pi/180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0] + ".png")
        save_extension(screen,"anim/"+name+"%03d"%count_frames+".png")
        count_frames += 1
    if(num_frames != 1):
        make_animation(name)
            # end operation loop
