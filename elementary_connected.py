import cairo, sys, argparse
import math, random, copy
from PIL import Image

float_gen = x = lambda a, b: random.uniform(a, b)

# Favorites: 73
rules = {
    (1, 1, 1):0,
    (1, 1, 0):1,
    (1, 0, 1):0,
    (1, 0, 0):1,
    (0, 1, 1):1,
    (0, 1, 0):0,
    (0, 0, 1):1,
    (0, 0, 0):0
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

pallete3 = [
    (170, 212, 203),
    (155, 143, 129),
    (244, 229, 207)
]

pallete4 = [
    (244,188, 97),
    (157, 155, 157),
    (229, 122, 111)
]

pallete5 = [
    (0, 0, 0)
]

backgrounds = [
   (243, 236, 205), # flesh like color
   (50, 50, 50),
   (107, 117, 111),
   (75, 80, 90)
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
    c = random.choice(pallete3)
    cr.set_source_rgb(c[0]/255.0, c[1]/255.0, c[2]/255.0)
    cr.set_line_width(2)
    cr.move_to(x, y)
    cr.curve_to(x1, y1, x2, y2, x3, y3)
    cr.stroke()

def draw_connected_line(cr, x1, y1, x2, y2, size, c):
    cr.move_to(x1, y1)
    cr.set_line_width(size)
    cr.set_source_rgb(c[0]/255.0, c[1]/255.0, c[2]/255.0)
    cr.line_to(x2, y2)
    cr.stroke()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify an image width", default=3000, type=int)
    parser.add_argument("--height", help="Specify an image height", default=3000, type=int)
    parser.add_argument("-cs", "--circlesize", help="Choose to draw orbits", default=5, type=int)
    parser.add_argument("-nb", "--numberbeziers", help="Choose to draw lines for the orbits", default=200, type=int)
    parser.add_argument("-ls", "--linesize", help="Specify an image height", default=5, type=int)
    args = parser.parse_args()
    
    
    
    width, height = args.width, args.height
    number_beziers = args.numberbeziers
    circle_size = args.circlesize
    line_size = args.linesize
    x_d = width/number_beziers
    y_d = x_d
    
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)
    
    draw_background(cr, backgrounds[3][0]/255.0, backgrounds[3][1]/255.0, backgrounds[3][2]/255.0, width, height)

    current_row = []
    for i in range(0, number_beziers):
        alive = int(random.getrandbits(1))
        c = random.choice(pallete3)
        current_row.append((alive, pallete3.index(c)))

#    current_row.append(0)
#    current_row[50] = 1
#    current_row[150] = 1

    next_row = copy.deepcopy(current_row)
    for k in range(y_d-y_d/7, height, y_d):
        
        # Determine the next row state by comparing rules
        for j in range(0, len(current_row)-2):
            alive = rules[(current_row[j][0], current_row[j+1][0], current_row[j+2][0])]
            c = random.choice(pallete3)
            next_row[j+1] = (alive, pallete3.index(c))
        alive = rules[(current_row[len(current_row)-1][0], current_row[0][0], current_row[1][0])]
        c = random.choice(pallete3)
        next_row[0] = (alive, pallete3.index(c))
        alive = rules[(current_row[len(current_row)-2][0], current_row[len(current_row)-1][0], current_row[0][0])]
        next_row[len(next_row)-1] = (alive, pallete3.index(c))

        # Draw connecting lines and the next row of circles
        if (k > y_d):
            for i in range(0, len(next_row)):
                if (next_row[i][0] is 1 and current_row[i][0] is 1):
                    if (next_row[i][1] is current_row[i][1]):
                        draw_connected_line(cr, i * x_d, k, i * x_d, k - y_d, line_size, pallete3[next_row[i][1]])

        for i in range(1, len(next_row)):
            if (i > 1):
                if (next_row[i][0] is 1 and next_row[i-1][0] is 1):
                    if (next_row[i][1] is next_row[i-1][1]):
                        draw_connected_line(cr, i * x_d, k, (i-1) * x_d, k, line_size, pallete3[next_row[i][1]])
            if (next_row[i][0] is 1):
                draw_circle_fill(cr, i * x_d, k, circle_size, pallete3[next_row[i][1]][0]/255.0, pallete3[next_row[i][1]][1]/255.0, pallete3[next_row[i][1]][2]/255.0)


        current_row = copy.deepcopy(next_row)
    ims.write_to_png('base.png')

if __name__ == "__main__":
    main()

