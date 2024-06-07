import PIL.Image, PIL.ImageDraw;
import math;
import random as ran;
import numpy as np;

ran.seed(389455756344565); # set seed for comparison between techniques

# a and b are the values to interpolate between, c is the (0-1) location between them which you wish to interpolate to.
def interpolate(a, b, c):
    c = 3*c*c - 2*c*c*c; # smoothstep

    return a + c * (b-a); # lerp



def perlin_2D(gradient_length, points_length):
    # Initialise 2D array of gradient vectors. (2D array of a 1D object, making it a 3D array of scalar values)
    gradients = [];
    for x in range(gradient_length):
        # has to be recreated each time because pointers

        current_column = [];
        for y in range(gradient_length):
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

    # Initialise 2D array of points.
    points = []
    for x in range(points_length):
        # has to be recreated each time because pointers

        current_column = [];
        for y in range(points_length):
            # get the coords of the relevant quadrant of gradient vectors (as in, the group of 4 gradient vectors which surround the point)

            grad_space_x = (float(x) / float(points_length)) * float(gradient_length - 1);
            grad_space_y = (float(y) / float(points_length)) * float(gradient_length - 1); # scale to gradient space (in other words, account for the (gradient & point) arrays having different lengths). It uses (gradient_length - 1) because there needs to be a row of gradient vectors beyond the last row of points to be able to form a quad with the far edge.

            quadrant_x = int(grad_space_x);
            quadrant_y = int(grad_space_y); # floor (with int()), as we want a whole number of gradient-vectors across. As we're flooring, we get the quadrant's coordinates which are closest to the origin. As all points are positive, this will be the bottom-left corner

            quadrant = [ gradients[quadrant_x][quadrant_y  ], gradients[quadrant_x + 1][quadrant_y    ],
                        gradients[quadrant_x][quadrant_y+1], gradients[quadrant_x + 1][quadrant_y + 1] ] # each gradient vector of the quadrant

            offset_vector = [ [grad_space_x - quadrant_x, grad_space_y -  quadrant_y     ], [grad_space_x - (quadrant_x + 1), grad_space_y -  quadrant_y     ],
                            [grad_space_x - quadrant_x, grad_space_y - (quadrant_y + 1)], [grad_space_x - (quadrant_x + 1), grad_space_y - (quadrant_y + 1)] ] # distance from each gradient vector in gradient space

            grad_offset_dot = []
            for i in range(len(offset_vector)):
                grad_offset_dot.append(quadrant[i][0] * offset_vector[i][0] + quadrant[i][1] * offset_vector[i][1]); # compute the dot product of each grad vector & dot vector & append it to grad_offset_dot

            # interpolate along
            a = interpolate(grad_offset_dot[0], grad_offset_dot[1], grad_space_x - quadrant_x);
            b = interpolate(grad_offset_dot[2], grad_offset_dot[3], grad_space_x - quadrant_x);

            # interpolate across & append to current_column
            current_column.append(interpolate(a, b, grad_space_y - quadrant_y));

        points.append(current_column);
    return points

def perlin_1D(gradient_length, points_length):
    gradients = []
    for x in range(gradient_length):
        grad = ran.uniform(-1, 1); # random either -1 or 1, skipping 0 due to the step size of 2
        gradients.append(grad);

    points = []
    for x in range(points_length):
        grad_space_x = (float(x) / float(points_length)) * float(gradient_length - 1);

        quadrant_x = int(grad_space_x); # is a 1D quadrant still a quadrant? Whatever, I'm trying to keep my variable names the same

        quadrant = [ gradients[quadrant_x], gradients[quadrant_x + 1] ]

        offset_values = [ grad_space_x - quadrant_x, grad_space_x - (quadrant_x + 1) ]

        grad_offset_dot = []
        for i in range(len(offset_values)):
            grad_offset_dot.append(quadrant[i] * offset_values[i]); # compute the dot product of each grad vector & dot vector & append it to grad_offset_dot... except it's scalar so it's just mutliplication in this case

        points.append(interpolate(grad_offset_dot[0], grad_offset_dot[1], grad_space_x - quadrant_x));

    return points;

# Surface gen (perlin output representing height)
lacunarity = 2; # octave-by-octave increase in frequency
persistance = 0.25; # octave-by-octave decrease in amplitude
num_octaves = 8;
points_length = 256;
surface_points = None;
has_already_started = False; # whether or not points has already been created
for n in range(num_octaves):
    frequency = lacunarity ** n; # for more *frequent* changes, we just need to increase the number of gradients in the space
    amplitude = persistance ** n;

    current_points = np.array(perlin_1D(6 * frequency, points_length)) * amplitude; # NOTE: As this is a numpy array, it multiplies component-wise, rather than repeating the array (as python does)

    if has_already_started != True: surface_points = current_points;
    else: surface_points = np.add(surface_points, current_points);

    has_already_started = True;

# Cave gen (perlin output representing density)
lacunarity = 2; # octave-by-octave increase in frequency
persistance = 0.25; # octave-by-octave decrease in amplitude
num_octaves = 8;
cave_points = None;
has_already_started = False; # whether or not points has already been created
for n in range(num_octaves):
    frequency = lacunarity ** n; # for more *frequent* changes, we just need to increase the number of gradients in the space
    amplitude = persistance ** n;

    current_points = np.array(perlin_2D(6 * frequency, points_length)) * amplitude; # NOTE: As this is a numpy array, it multiplies component-wise, rather than repeating the array (as python does)

    if has_already_started != True: cave_points = current_points;
    else: cave_points = np.add(cave_points, current_points);

    has_already_started = True;


terrain_height_variance = 0.3; # this is a fraction of the points_length (aka the resolution), representing the difference between the minimum and maximum surface height
terrain_height = 0.05; # this is a fraction of the points_length (aka the resolution), representing how much air there should be over the maximum suruface height. Half of terrain_height_variance is added because half of it is negative.
surface_points = surface_points * (terrain_height_variance * points_length) + ((terrain_height + terrain_height_variance / 2) * points_length)

# drawing
img = PIL.Image.new(mode='RGB', size=(points_length, points_length), color=(128, 0, 128)); # set it as an odd shade of purple - that's no way near any colour I'm expecting, so it should be obvious if any of the image isn't filled for some reason

sky_colour = (64, 64, 192);
underground_air_colour = (32, 32, 48);
stone_colour = (128, 128, 128);
grass_colour = (64, 128, 64);
dirt_colour = (128, 80, 48);

max_density_for_air = 0.3; # assume higher value -> less dense.
dirt_layers = 3;

canvas = PIL.ImageDraw.Draw(img); # get the canvas for the image
for x in range(points_length): # draw every pixel according to specs
    for y in range(points_length):
        if surface_points[x] > y: # if this pixel is above the surface, it's in the sky
            canvas.point(xy=(x, y), fill=sky_colour);

        elif cave_points[x][y] > max_density_for_air: # if it's not dense enough to be stone, it's air (in this example, where air is just the absence of stone)
            canvas.point(xy=(x, y), fill=underground_air_colour);
        else: canvas.point(xy=(x, y), fill=stone_colour);

        if int(surface_points[x]) == y and not cave_points[x][y] > max_density_for_air:
            canvas.point(xy=(x, y), fill=grass_colour);

        # if it's in one of the few rows below (remember - lower values are higher) the grass AND it's not a cave entrance, it's dirt.
        elif int(surface_points[x]) < y and int(surface_points[x]) + dirt_layers > y and not cave_points[x][y] > max_density_for_air:
            canvas.point(xy=(x, y), fill=dirt_colour);





img.save('cave_example.png');
img.show();
