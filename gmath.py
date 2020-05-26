import math
from display import *

  # Ambient light is represeneted by a color value
  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.
  # Reflection constants (ka, kd, ks) are represened as arrays of doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

def get_lighting(normal, view, ambient, light, symbols, reflect):
    n = normal[:]
    normalize(n)
    normalize(light[LOCATION])
    normalize(view)
    r = symbols[reflect][1]

    a = calculate_ambient(ambient, r)
    d = calculate_diffuse(light, r, n)
    s = calculate_specular(light, r, view, n)

    i = [0, 0, 0]
    i[RED] = int(a[RED] + d[RED] + s[RED])
    i[GREEN] = int(a[GREEN] + d[GREEN] + s[GREEN])
    i[BLUE] = int(a[BLUE] + d[BLUE] + s[BLUE])
    limit_color(i)
    return i

def calculate_ambient(alight, reflect):
    a = [0, 0, 0]
    a[RED] = alight[RED] * reflect['red'][AMBIENT]
    a[GREEN] = alight[GREEN] * reflect['green'][AMBIENT]
    a[BLUE] = alight[BLUE] * reflect['blue'][AMBIENT]
    return a

def calculate_diffuse(light, reflect, normal):
    d = [0, 0, 0]
    dot = dot_product(light[LOCATION], normal)
    dot = dot if dot > 0 else 0
    d[RED] = light[COLOR][RED] * reflect['red'][DIFFUSE] * dot
    d[GREEN] = light[COLOR][GREEN] * reflect['green'][DIFFUSE] * dot
    d[BLUE] = light[COLOR][BLUE] * reflect['blue'][DIFFUSE] * dot
    return d

def calculate_specular(light, reflect, view, normal):
    s = [0, 0, 0]
    n = [0, 0, 0]
    result = 2 * dot_product(light[LOCATION], normal)

    n[0] = normal[0] * result - light[LOCATION][0]
    n[1] = normal[1] * result - light[LOCATION][1]
    n[2] = normal[2] * result - light[LOCATION][2]

    result = dot_product(n, view)
    result = result if result > 0 else 0
    result = pow( result, SPECULAR_EXP )

    s[RED] = light[COLOR][RED] * reflect['red'][SPECULAR] * result
    s[GREEN] = light[COLOR][GREEN] * reflect['green'][SPECULAR] * result
    s[BLUE] = light[COLOR][BLUE] * reflect['blue'][SPECULAR] * result
    return s

def limit_color(color):
    color[RED] = 255 if color[RED] > 255 else color[RED]
    color[GREEN] = 255 if color[GREEN] > 255 else color[GREEN]
    color[BLUE] = 255 if color[BLUE] > 255 else color[BLUE]

#------------------------------------------------------------------------------#

def normalize(vector): #should modify the parameter
    magnitude = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def calculate_normal(polygons, i): #Calculate surface normal for triangle whose first point is index i
    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]
    for j in range(0, 3):
        A[j] = polygons[i + 1][j] - polygons[i][j]
        B[j] = polygons[i + 2][j] - polygons[i][j]
    for j in range(0, 3):
        N[j] = A[(j + 1) % 3] * B[(j + 2) % 3] - A[(j + 2) % 3] * B[(j + 1) % 3]
    return N
