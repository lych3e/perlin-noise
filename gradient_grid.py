import pygame; # PIL's line drawing doesn't have antialiasing, this was the next-best option
import random as ran;
import math;


scale_factor = 4;
quadrant_length = 20; # size of each square
gradient_length = 10; # length of the gradient lines
grid_width = 5; # number of quadrants in the x direction
grid_height = 5; # number of quadrants in the y direction
background_colour = (255, 255, 255);
grid_colour = (0, 0, 0);
gradient_colour = (255, 0, 0);

quadrant_length *= scale_factor;
gradient_length *= scale_factor;

# Initialise 2D array of gradient vectors. (2D array of a 1D object, making it a 3D array of scalar values)
gradients = [];
for x in range(grid_width + 1): # +1 because we need a gradient at the end too
    # has to be recreated each time because pointers

    current_column = [];
    for y in range(grid_height + 1): # +1 because we need a gradient at the end too
        mag = 0; # scope fix
        v = None; # scope fix

        while (mag == 0): # the gradient needs to point in a direction, so repeat if the magnitude ends up being zero.
            # create the gradient vector
            v = [];
            v.append(ran.uniform(-1, 1)); # add values to vector
            v.append(ran.uniform(-1, 1));

            # normalise the gradient vector
            mag = math.sqrt(v[0] * v[0] + v[1] * v[1]); # get the magnitude of the vector

        v[0] /= mag;
        v[1] /= mag;

        current_column.append(v);

    gradients.append(current_column);

img_W = grid_width*quadrant_length + 1 + quadrant_length * 2;
img_H = grid_height*quadrant_length + 1 + quadrant_length * 2;

# drawing
#img = PIL.Image.new(mode='RGB', size=(img_W, img_H), color=background_colour); # set it as an odd shade of purple - that's no way near any colour I'm expecting, so it should be obvious if any of the image isn't filled for some reason
pygame.init();
canvas = pygame.display.set_mode(size=(img_W, img_H), depth=8);

canvas.fill(background_colour);

#canvas = PIL.ImageDraw.Draw(img); # get the canvas for the image

# draw gradients
for a in range(grid_width + 1): # +1 because we need a gradient at the end too
    for b in range(grid_height + 1): # +1 because we need a gradient at the end too
        v = gradients[a][b];

        x = quadrant_length + a * quadrant_length;
        y = quadrant_length + b * quadrant_length;

        #canvas.line(xy=[(x, y), (x + v[0] * gradient_length, y + v[1] * gradient_length)], fill=gradient_colour, width=1);
        pygame.draw.aaline(canvas, gradient_colour, (x, y), (x + v[0] * gradient_length, y + v[1] * gradient_length));


# draw grid
for y in range(grid_height + 1):
    pygame.draw.aaline(canvas, grid_colour, (quadrant_length, y*quadrant_length + quadrant_length), (img_W-quadrant_length, y*quadrant_length + quadrant_length));

for x in range(grid_width + 1):
    pygame.draw.aaline(canvas, grid_colour, (x*quadrant_length + quadrant_length, quadrant_length), (x*quadrant_length + quadrant_length, img_H-quadrant_length));


pygame.display.flip(); # display what we've drawn
pygame.image.save(canvas, 'gradient_grid.png');
input();
