import matplotlib.pyplot as plot;
import math;
import random as ran;
import numpy as np;

ran.seed(38456456); # set seed for comparison between techniques

# a and b are the values to interpolate between, c is the (0-1) location between them which you wish to interpolate to.
def interpolate(a, b, c):
    c = 3*c*c - 2*c*c*c; # smoothstep

    return a + c * (b-a); # lerp



def perlin(gradient_length, points_length):
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

lacunarity = 2; # octave-by-octave increase in frequency
persistance = 0.25; # octave-by-octave decrease in amplitude
num_octaves = 8;
points_length = 512;
points = None;
has_already_started = False; # whether or not points has already been created
for n in range(num_octaves):
    frequency = lacunarity ** n; # for more *frequent* changes, we just need to increase the number of gradients in the space
    amplitude = persistance ** n;

    current_points = np.array(perlin(3 * frequency, points_length)) * amplitude; # NOTE: As this is a numpy array, it multiplies component-wise, rather than repeating the array (as python does)

    if has_already_started != True: points = current_points;
    else: points = np.add(points, current_points);

    has_already_started = True;

# display
x = np.arange(0, points_length, 1);
X, Y = np.meshgrid(x, x);

graph = plot.figure().add_subplot(projection='3d');
graph.plot_surface(X, Y, points, cmap='terrain', rcount=128, ccount=128);
graph.set_proj_type('persp');

graph.view_init(elev=60.0);

plot.savefig('perlin_2D_octaves.png');
plot.show();
