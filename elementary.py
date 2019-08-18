import cairo, sys, argparse
import math, random, copy

float_gen = x = lambda a, b: random.uniform(a, b)

# Favorites: 73
rules = {
    (1, 1, 1):0,
    (1, 1, 0):1,
    (1, 0, 1):0,
    (1, 0, 0):0,
    (0, 1, 1):1,
    (0, 1, 0):0,
    (0, 0, 1):0,
    (0, 0, 0):1
}

pallete1 = [
    (112, 181, 171),
    (220, 109, 71),
    (240, 204, 170)
]

pallete2 = [
    (106, 154, 172),
    (146, 189, 144),
    (130, 179, 176)
]

backgrounds = [
               (243, 236, 205), # flesh like color
               (50, 50, 50)
]



def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0,0,width,height)
    cr.fill()

def draw_circle_fill(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.fill()

def draw_bezier(cr, x, y, x1, y1, x2, y2, x3, y3):
    c = random.choice(pallete1)
    cr.set_source_rgb(c[0]/255.0, c[1]/255.0, c[2]/255.0)
    cr.set_line_width(2)
    cr.move_to(x, y)
    cr.curve_to(x1, y1, x2, y2, x3, y3)
    cr.stroke()

def main():
    width, height = 3000, 3000
    number_beziers = 200
    circle_size = 5
    x_d = width/number_beziers
    y_d = x_d
    
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)
    
    draw_background(cr, backgrounds[1][0]/255.0, backgrounds[1][1]/255.0, backgrounds[1][2]/255.0, width, height)

    current_row = []
    for i in range(0, number_beziers):
        current_row.append(int(random.getrandbits(1)))
#        current_row.append(0)
#    current_row[50] = 1
#    current_row[150] = 1

    next_row = copy.deepcopy(current_row)
    for k in range(y_d, height, y_d):
        # Determine the next row state by comparing rules
        for j in range(0, len(current_row)-2):
            next_row[j+1] = rules[(current_row[j], current_row[j+1], current_row[j+2])]
        next_row[0] = rules[(current_row[len(current_row)-1], current_row[0], current_row[1])]
        next_row[len(next_row)-1] = rules[(current_row[len(current_row)-2], current_row[len(current_row)-1], current_row[0])]

        # Iterate through and draw the circles
        for i in range(1, len(next_row)):
            if (next_row[i] is 1):
                c = random.choice(pallete1)
                draw_circle_fill(cr, i * x_d, k, circle_size, c[0]/255.0, c[1]/255.0, c[2]/255.0)
        current_row = copy.deepcopy(next_row)
    ims.write_to_png('base.png')

if __name__ == "__main__":
    main()
