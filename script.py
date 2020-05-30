import mdl, math
from display import *
from matrix import *
from draw import *

def first_pass(commands):
    name = ''
    num_frames = 1
    vary = False;
    for command in commands: #Checks commands array for animation commands (frames, basename, vary)
        c = command['op']
        args = command['args']
        if c == "vary":
            vary = True;
        elif c == "basename": #sets num_frames and basenames if present
            name = args[0]
        elif c == "frames":
            num_frames = int(args[0])
    if name == '': #If no basename, name is set to default with printed message with name
        print("Warning! No Basename provided. Default Basename: img")
        name = "img"
    if (num_frames == 1) and vary: #If vary is found, but not frames, entire program exits
        print("Compiler Error: Expected more than one frame for Vary command")
        exit()
    return (name, num_frames)

def second_pass(commands, num_frames):
    frames = [{} for i in range(num_frames)] #each index, or frame, has dictionary of knob values with knob name as key
    for command in commands:
        if command['op'] == "vary": #goes from 0 to frames - 1 and adds to dictionary with correct value
            args = command['args']
            if num_frames > 1:
                start = int(args[0])
                end = int(args[1])
                value1 = args[2]
                value2 = args[3]
                knob = command['knob']
                if args[4] == "linear":
                    v = (1.0 * value2 - value1) / (end - start)
                    for i in range(start, end + 1):
                        frames[i][knob] = v * (i - start) + value1
                elif args[4] == "accelerate":
                    a = 2 * (1.0 * value2 - value1) / (end - start) ** 2
                    for i in range(start, end + 1):
                        frames[i][knob] = 0.5 * a * (i - start) ** 2 + value1
                elif args[4] == "decelerate":
                    a = -2 * (1.0 * value2 - value1) / (end - start) ** 2
                    vi = -1 * a * (end - start)
                    for i in range(start, end + 1):
                        frames[i][knob] = 0.5 * a * (i - start) ** 2 + vi * (i - start) + value1
                elif args[4] == "pause":
                    mid = (start + end) // 2
                    avg = (value1 + value2) / 2.0
                    a = -2 * (1.0 * avg - value1) / (mid - start) ** 2
                    vi = -1 * a * (mid - start)
                    for i in range(start, end + 1):
                        frames[i][knob] = 0.5 * a * (i - start) ** 2 + vi * (i - start) + value1
                        if i == mid:
                            a *= -1
                            vi = 0
                            value1 = avg
                            start = mid if (start - end) % 2 == 0 else mid + 1
                elif args[4] == "cosine":
                    for i in range(start, end + 1):
                        ratio = math.cos(math.pi * (i - start) / (end - start))
                        frames[i][knob] = (value2 - value1) * ((ratio - 1) / -2) + value1
                elif args[4] == "sine":
                    for i in range(start, end + 1):
                        ratio = math.sin(math.pi * (i - start) / (end - start))
                        frames[i][knob] = (value2 - value1) * ratio + value1
                elif args[4] == "bouncing":
                    bounces = int(args[5]) if len(args) > 5 else 1 #bounce of 0 means that it just drops
                    if bounces < 0:
                        print("Compiler Error: Expected number of bounces to be a positive integer")
                        exit()
                    decay = args[6] if len(args) > 6 else 0.5 #the decay of height
                    for i in range(start, end + 1):
                        (r, t, frac, num) = bounce_info(bounces, decay, i, start, end, value1, value2)
                        lower = 2 * t * (1 - r ** num) / (1 - r)
                        upper = lower + 2 * t * r ** num
                        p = (frac + t - lower) / (upper - lower)
                        a = -2.0 * (value2 - value1) / (0.5) ** 2
                        vi = a / -2.0
                        frames[i][knob] = 0.5 * a * p ** 2 + vi * p
                        print(str(p) + ", " + str(frames[i][knob]))
    return frames

def bounce_info(bounces, decay, i, start, end, value1, value2):
    r = math.sqrt(decay)
    t = (value2 - value1) / (1 + (2 * r * (1 - r ** bounces)) / (1 - r))
    frac = (i - start) / (end - start) #t is amount of time for drop until first bounce
    cur = t
    num = 1 #what bounce number it is on right now
    run = True
    while run:
        if cur > frac:
            run = False
            num = num - 1 if num <= bounces + 1 else num - 2
        else:
            cur += 2 * t * (r ** num)
            num += 1
    return (r, t, frac, num)

def run(filename): #runs an mdl script
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0, 0, 1];
    ambient = [50, 50, 50]
    light = [[0.5, 0.75, 1], [255, 255, 255]]
    color = [0, 0, 0]
    symbols['.white'] = ['constants', {'red':[0.2, 0.5, 0.5], 'green':[0.2, 0.5, 0.5], 'blue':[0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)
    count_frames = 0

    while count_frames < num_frames:
        print("Creating Frame #" + str(count_frames))
        tmp = new_matrix()
        ident(tmp)
        stack = [[x[:] for x in tmp]]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        for command in commands:
            c = command['op']
            args = command['args']
            knob_value = 1
            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp, args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult(stack[-1], tmp)
                add_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp, args[0], args[1], args[2], args[3], step_3d)
                matrix_mult(stack[-1], tmp)
                add_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult(stack[-1], tmp)
                add_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'cylinder':
                if command['constants']:
                    reflect = command['constants']
                add_cylinder(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult(stack[-1], tmp)
                add_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'cone':
                if command['constants']:
                    reflect = command['constants']
                add_cone(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult(stack[-1], tmp)
                add_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'mesh':
                if command['constants']:
                    reflect = command['constants']
                (points, order) = mdl.objParse(command['cs'] + ".obj")
                makeMesh(tmp, points, order)
                matrix_mult(stack[-1], tmp)
                add_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp, args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult(stack[-1], tmp)
                add_lines(tmp, screen, zbuffer, color)
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
                theta = args[1] * (math.pi / 180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]])
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0] + ".png")
        save_extension(screen, "anim/" + name + "%03d" % count_frames + ".png")
        count_frames += 1
    if num_frames != 1:
        make_animation(name)
