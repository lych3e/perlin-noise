import matplotlib.pyplot as plot;
import math;
import random as ran;
import numpy as np;

ran.seed(389455756344565); # set seed for comparison between techniques

# a and b are the values to interpolate between, c is the (0-1) location between them which you wish to interpolate to.
def interpolate(a, b, c):
    c = 3*c*c - 2*c*c*c; # smoothstep

    return a + c * (b-a); # lerp

def perlin(gradient_length, points_length):
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
plot.plot(range(points_length), points);
plot.savefig('perlin_1D_octaves.png');
plot.show();
