#!/bin/env/python

from kynetix.utilities.coordinate_utilities import CoordsGroup

coords_indices = [
    ([0.0, 0.0, 0.0], 0), ([0.5, 0.0, 0.0], 1), ([1.0, 0.0, 0.0], 0), ([1.5, 0.0, 0.0], 1),
    ([2.0, 0.0, 0.0], 0), ([2.5, 0.0, 0.0], 1), ([3.0, 0.0, 0.0], 0), ([0.0, 0.5, 0.0], 2),
    ([1.0, 0.5, 0.0], 2), ([2.0, 0.5, 0.0], 2), ([3.0, 0.5, 0.0], 2), ([0.0, 1.0, 0.0], 0),
    ([0.5, 1.0, 0.0], 1), ([1.0, 1.0, 0.0], 0), ([2.0, 1.0, 0.0], 0),
    ([2.5, 1.0, 0.0], 1), ([3.0, 1.0, 0.0], 0), ([0.0, 1.5, 0.0], 2), ([1.0, 1.5, 0.0], 2),
    ([2.0, 1.5, 0.0], 2), ([3.0, 1.5, 0.0], 2), ([0.0, 2.0, 0.0], 0), ([0.5, 2.0, 0.0], 1),
    ([2.5, 2.0, 0.0], 1), ([3.0, 2.0, 0.0], 0), ([0.0, 2.5, 0.0], 2), ([1.0, 2.5, 0.0], 2),
    ([2.0, 2.5, 0.0], 2), ([3.0, 2.5, 0.0], 2), ([0.0, 3.0, 0.0], 0), ([0.5, 3.0, 0.0], 1),
    ([1.0, 3.0, 0.0], 0), ([2.0, 3.0, 0.0], 0), ([2.5, 3.0, 0.0], 1), ([3.0, 3.0, 0.0], 0),
    ([0.0, 3.5, 0.0], 2), ([1.0, 3.5, 0.0], 2), ([2.0, 3.5, 0.0], 2), ([3.0, 3.5, 0.0], 2),
    ([0.0, 4.0, 0.0], 0), ([0.5, 4.0, 0.0], 1), ([1.0, 4.0, 0.0], 0), ([1.5, 4.0, 0.0], 1),
    ([2.0, 4.0, 0.0], 0), ([2.5, 4.0, 0.0], 1), ([3.0, 4.0, 0.0], 0), ([3.5, 4.0, 0.0], 1),
    ([4.0, 4.0, 0.0], 0)
]

rxn_expression = "CO_b + O_b <-> OC-O_2b -> CO2_g + 2*_b"

# Coordinates of origin.
ori_coords = [[1.0, 2.0, 0.0], [1.5, 2.0, 0.0], [1.0, 2.5, 0.0]]

# Get fixed coord_groups.
c = [[0.0, 0.0, 0.0],
     [0.5, 0.5, 0.0], 
     [1.0, 0.0, 0.0], 
     [0.5, -0.5, 0.0],
     [0.5, 0.0, 0.0]]
e = ["V", "V", "V", "V", "O_s"]
O_s = CoordsGroup(c, e)

c = [[0.0, 0.0, 0.0],
     [0.5, 0.5, 0.0], 
     [1.0, 0.0, 0.0], 
     [0.5, -0.5, 0.0],
     [0.5, 0.0, 0.0]]
e = ["V", "V", "V", "V", "V"]
free1 = CoordsGroup(c, e).move([0, 1, 0])
free2 = CoordsGroup(c, e).move([0, -1, 0])

coord_groups = [[O_s, free1], [O_s, free2]]

