import math

"""A matrix will be an N sized list of [x, y, z, 1] lists.
For multiplication, consider the lists like so:
x0  x1 ... xn
y0  y1 ... yn
z0  z1 ... zn
1   1  ... 1"""

def make_bezier():
    return [[-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]]

def make_hermite():
    return [[2, -3, 0, 1],
            [-2, 3, 0, 0],
            [1, -2, 1, 0],
            [1, -1, 0, 0]]

def generate_curve_coefs(p0, p1, p2, p3, t):
    coefs = [[p0, p1, p2, p3]]
    if t == 'hermite':
        curve = make_hermite()
    else:
        curve = make_bezier()
    matrix_mult(curve, coefs)
    return coefs

def make_translate(x, y, z):
    t = new_matrix()
    ident(t)
    t[3][0] = x
    t[3][1] = y
    t[3][2] = z
    return t

def make_scale(x, y, z):
    t = new_matrix()
    ident(t)
    t[0][0] = x
    t[1][1] = y
    t[2][2] = z
    return t

def make_rotX(theta):
    t = new_matrix()
    ident(t)
    t[1][1] = math.cos(theta)
    t[2][1] = -1 * math.sin(theta)
    t[1][2] = math.sin(theta)
    t[2][2] = math.cos(theta)
    return t

def make_rotY(theta):
    t = new_matrix()
    ident(t)
    t[0][0] = math.cos(theta)
    t[0][2] = -1 * math.sin(theta)
    t[2][0] = math.sin(theta)
    t[2][2] = math.cos(theta)
    return t

def make_rotZ(theta):
    t = new_matrix()
    ident(t)
    t[0][0] = math.cos(theta)
    t[1][0] = -1 * math.sin(theta)
    t[0][1] = math.sin(theta)
    t[1][1] = math.cos(theta)
    return t

#------------------------------------------------------------------------------#

def print_matrix(matrix):
    s = ''
    for r in range(len(matrix[0])):
        for c in range(len(matrix)):
            s += str(matrix[c][r]) + ' '
        s += '\n'
    print(s)

def ident(matrix):
    for r in range(len(matrix[0])):
        for c in range(len(matrix)):
            matrix[c][r] = 1 if r == c else 0

def matrix_mult(m1, m2): #multiply m1 by m2, modifying m2 to be the product
    point = 0
    for row in m2:
        tmp = row[:] #get a copy of the next point
        for r in range(4):
            m2[point][r] = 0
            for c in range(4):
                m2[point][r] += m1[c][r] * tmp[c]
        point += 1

def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range(cols):
        m.append([])
        for r in range(rows):
            m[c].append(0)
    return m
