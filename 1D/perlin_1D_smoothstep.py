import matplotlib.pyplot as plot;
import math;
import random as ran;
import numpy as np;

ran.seed(389455756344565); # set seed for comparison between techniques

# a and b are the values to interpolate between, c is the (0-1) location between them which you wish to interpolate to.
def interpolate(a, b, c):
    c = 3*c*c - 2*c*c*c; # smoothstep

    return a + c * (b-a); # lerp


gradient_length = 6;

gradients = []
for x in range(gradient_length):
    grad = ran.uniform(-1, 1); # random either -1 or 1, skipping 0 due to the step size of 2
    gradients.append(grad);


points_length = 512;

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

# display
plot.plot(range(points_length), points);
plot.savefig('perlin_1D_smoothstep.png');
plot.show();
