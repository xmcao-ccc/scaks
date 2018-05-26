# KMC processes.
processes = [
    # CO adsorbed at top site.
    {
        "reaction": "CO_g + *_t -> CO_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                              [-0.5, 0.0, 0.0],
                              [-0.5, 0.5, 0.0],
                              [0.0, 0.5, 0.0],
                              [0.5, 0.5, 0.0],
                              [0.5, 0.0, 0.0],
                              [0.5, -0.5, 0.0],
                              [0.0, -0.5, 0.0],
                              [-0.5, -0.5, 0.0]]],
        "elements_before": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["C", "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    # CO adsorbed on bridge site.
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0]]],
        "elements_before": ["V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "C"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0]]],
        "elements_before": ["V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "C"],
        "basis_sites": [0],
    },

    # O2 adsorbed lying.
    {
        "reaction": "O2_g + 2*_t -> O2_2t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.0, -0.5, 0.0],
                               [-0.5, -0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [1.0, 0.5, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.5, 0.0, 0.0],
                               [1.5, -0.5, 0.0],
                               [1.0, -0.5, 0.0]]],
        "elements_before": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['O_r', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_l', 'V', 'V', 'V', 'V', 'V'],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_t -> O2_2t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.0, -0.5, 0.0],
                               [-0.5, -0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [-0.5, 1.0, 0.0],
                               [-0.5, 1.5, 0.0],
                               [0.0, 1.5, 0.0],
                               [0.5, 1.5, 0.0],
                               [0.5, 1.0, 0.0]]],
        "elements_before": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['O_u', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_d', 'V', 'V', 'V', 'V', 'V'],
        "basis_sites": [0],
    },

    # O2 dissociation directly.
    {
        "reaction": "O2_2t + 2*_b <-> O-O_2t + 2*_b -> 2O_b + 2*_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [1.0, 0.5, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.5, 0.0, 0.0],
                               [1.5, -0.5, 0.0],
                               [1.0, -0.5, 0.0],
                               [2.0, 0.0, 0.0],
                               [2.0, 0.5, 0.0],
                               [2.5, 0.5, 0.0],
                               [2.5, 0.0, 0.0],
                               [2.5, -0.5, 0.0],
                               [2.0, -0.5, 0.0],
                               [3.0, 0.0, 0.0]]],
        "elements_before": ['V', 'V', 'O_r', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_l', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V'],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_2t + 2*_b <-> O-O_2t + 2*_b -> 2O_b + 2*_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [-0.5, 1.0, 0.0],
                               [-0.5, 1.5, 0.0],
                               [0.0, 1.5, 0.0],
                               [0.5, 1.5, 0.0],
                               [0.5, 1.0, 0.0],
                               [0.0, 2.0, 0.0],
                               [-0.5, 2.0, 0.0],
                               [-0.5, 2.5, 0.0],
                               [0.0, 2.5, 0.0],
                               [0.5, 2.5, 0.0],
                               [0.5, 2.0, 0.0],
                               [0.0, 3.0, 0.0]]],
        "elements_before": ['V', 'V', 'O_u', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_d', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V'],
        "basis_sites": [0],
    },
    # dissociation on adjacent bridge sites.
    {
        "reaction": "O2_g + 2*_b -> O_b + O_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.0, 0.5, 0.0]]],
        "elements_before": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_b -> O_b + O_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [1.0, 1.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.0, 0.5, 0.0]]],
        "elements_before": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_b -> O_b + O_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.5, 1.5, 0.0],
                               [1.0, 1.0, 0.0],
                               [0.5, 1.0, 0.0]]],
        "elements_before": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_b -> O_b + O_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [-1.0, 1.0, 0.0],
                               [-0.5, 1.5, 0.0],
                               [-0.5, 1.0, 0.0]]],
        "elements_before": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },

    # O2 adsorbed lying beside bridge CO.
    {
        "reaction": "O2_g + 2*_t -> O2_2t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-0.5, 0.0, 0.0],  # 1, 2, 3
                               [-0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 4, 5
                               [0.5, 0.5, 0.0], [1.0, 0.5, 0.0],  # 6, 7
                               [1.5, 0.5, 0.0], [1.5, 0.0, 0.0],  # 8, 9
                               [1.5, -0.5, 0.0], [1.0, -0.5, 0.0],  # 10, 11
                               [0.5, -0.5, 0.0], [0.0, -0.5, 0.0],  # 12, 13
                               [-0.5, -0.5, 0.0], [-1.0, 0.0, 0.0],  # 14, 15
                               [0.5, 0.0, 0.0]],  # 16
                              ],
        "elements_before": ["V", "V", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_r", "O_l", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_t -> O2_2t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.5, 0.0, 0.0],  # 1, 2, 3
                               [1.5, 0.5, 0.0], [1.0, 0.5, 0.0],  # 4, 5
                               [0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 6, 7
                               [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.0],  # 8, 9
                               [-0.5, -0.5, 0.0], [0.0, -0.5, 0.0],  # 10, 11
                               [0.5, -0.5, 0.0], [1.0, -0.5, 0.0],  # 12, 13
                               [1.5, -0.5, 0.0], [2.0, 0.0, 0.0],  # 14, 15
                               [0.5, 0.0, 0.0]],  # 16
                              ],
        "elements_before": ["V", "V", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_r", "O_l", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_t -> O2_2t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.5, 0.0],  # 1, 2, 3
                               [0.5, 0.5, 0.0], [0.5, 0.0, 0.0],  # 4, 5
                               [0.5, -0.5, 0.0], [0.5, -1.0, 0.0],  # 6, 7
                               [0.5, -1.5, 0.0], [0.0, -1.5, 0.0],  # 8, 9
                               [-0.5, -1.5, 0.0], [-0.5, -1.0, 0.0],  # 10, 11
                               [-0.5, -0.5, 0.0], [-0.5, 0.0, 0.0],  # 12, 13
                               [-0.5, 0.5, 0.0], [0.0, 1.0, 0.0],  # 14, 15
                               [0.0, -0.5, 0.0]],  # 16
                              ],
        "elements_before": ["V", "V", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_d", "O_u", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_t -> O2_2t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.5, 0.0],  # 1, 2, 3
                               [0.5, -1.5, 0.0], [0.5, -1.0, 0.0],  # 4, 5
                               [0.5, -0.5, 0.0], [0.5, 0.0, 0.0],  # 6, 7
                               [0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 8, 9
                               [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.0],  # 10, 11
                               [-0.5, -0.5, 0.0], [-0.5, -1.0, 0.0],  # 12, 13
                               [-0.5, -1.5, 0.0], [0.0, -2.0, 0.0],  # 14, 15
                               [0.0, -0.5, 0.0]],  # 16
                              ],
        "elements_before": ["V", "V", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_d", "O_u", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    # CO adsorbed lying beside bridge O2.
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.5, 0.0, 0.0],  # 1, 2, 3
                               [1.5, 0.5, 0.0], [1.0, 0.5, 0.0],  # 4, 5
                               [0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 6, 7
                               [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.0],  # 8, 9
                               [-0.5, -0.5, 0.0], [0.0, -0.5, 0.0],  # 10, 11
                               [0.5, -0.5, 0.0], [1.0, -0.5, 0.0],  # 12, 13
                               [1.5, -0.5, 0.0], [2.0, 0.0, 0.0],  # 14, 15
                               [0.5, 0.0, 0.0]],  # 16
                              ],
        "elements_before": ["O_r", "O_l", "V", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_r", "O_l", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-0.5, 0.0, 0.0],  # 1, 2, 3
                               [-0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 4, 5
                               [0.5, 0.5, 0.0], [1.0, 0.5, 0.0],  # 6, 7
                               [1.5, 0.5, 0.0], [1.5, 0.0, 0.0],  # 8, 9
                               [1.5, -0.5, 0.0], [1.0, -0.5, 0.0],  # 10, 11
                               [0.5, -0.5, 0.0], [0.0, -0.5, 0.0],  # 12, 13
                               [-0.5, -0.5, 0.0], [-1.0, 0.0, 0.0],  # 14, 15
                               [0.5, 0.0, 0.0]],  # 16
                              ],
        "elements_before": ["O_r", "O_l", "V", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_r", "O_l", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.5, 0.0],  # 1, 2, 3
                               [0.5, 0.5, 0.0], [0.5, 0.0, 0.0],  # 4, 5
                               [0.5, -0.5, 0.0], [0.5, -1.0, 0.0],  # 6, 7
                               [0.5, -1.5, 0.0], [0.0, -1.5, 0.0],  # 8, 9
                               [-0.5, -1.5, 0.0], [-0.5, -1.0, 0.0],  # 10, 11
                               [-0.5, -0.5, 0.0], [-0.5, 0.0, 0.0],  # 12, 13
                               [-0.5, 0.5, 0.0], [0.0, 1.0, 0.0],  # 14, 15
                               [0.0, -0.5, 0.0]],  # 16
                              ],
        "elements_before": ["O_d", "O_u", "V", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_d", "O_u", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.5, 0.0],  # 1, 2, 3
                               [0.5, -1.5, 0.0], [0.5, -1.0, 0.0],  # 4, 5
                               [0.5, -0.5, 0.0], [0.5, 0.0, 0.0],  # 6, 7
                               [0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 8, 9
                               [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.0],  # 10, 11
                               [-0.5, -0.5, 0.0], [-0.5, -1.0, 0.0],  # 12, 13
                               [-0.5, -1.5, 0.0], [0.0, -2.0, 0.0],  # 14, 15
                               [0.0, -0.5, 0.0]],  # 16
                              ],
        "elements_before": ["O_d", "O_u", "V", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["O_d", "O_u", "C", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    # O2 dissociation with CO.
    {
        "reaction": "O2_2t + CO_b <-> OCO-O_2t + *_b -> O_b + CO2_g + 2*_t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.5, 0.0, 0.0],  # 1, 2, 3
                               [1.5, 0.5, 0.0], [1.0, 0.5, 0.0],  # 4, 5
                               [0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 6, 7
                               [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.0],  # 8, 9
                               [-0.5, -0.5, 0.0], [0.0, -0.5, 0.0],  # 10, 11
                               [0.5, -0.5, 0.0], [1.0, -0.5, 0.0],  # 12, 13
                               [1.5, -0.5, 0.0], [2.0, 0.0, 0.0],  # 14, 15
                               [0.5, 0.0, 0.0]],  # 16
                              ],
        "elements_before": ["O_r", "O_l", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "O_s"],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_2t + CO_b <-> OCO-O_2t + *_b -> O_b + CO2_g + 2*_t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-0.5, 0.0, 0.0],  # 1, 2, 3
                               [-0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 4, 5
                               [0.5, 0.5, 0.0], [1.0, 0.5, 0.0],  # 6, 7
                               [1.5, 0.5, 0.0], [1.5, 0.0, 0.0],  # 8, 9
                               [1.5, -0.5, 0.0], [1.0, -0.5, 0.0],  # 10, 11
                               [0.5, -0.5, 0.0], [0.0, -0.5, 0.0],  # 12, 13
                               [-0.5, -0.5, 0.0], [-1.0, 0.0, 0.0],  # 14, 15
                               [0.5, 0.0, 0.0]],  # 16
                              ],
        "elements_before": ["O_r", "O_l", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "O_s"],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_2t + CO_b <-> OCO-O_2t + *_b -> O_b + CO2_g + 2*_t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.5, 0.0],  # 1, 2, 3
                               [0.5, 0.5, 0.0], [0.5, 0.0, 0.0],  # 4, 5
                               [0.5, -0.5, 0.0], [0.5, -1.0, 0.0],  # 6, 7
                               [0.5, -1.5, 0.0], [0.0, -1.5, 0.0],  # 8, 9
                               [-0.5, -1.5, 0.0], [-0.5, -1.0, 0.0],  # 10, 11
                               [-0.5, -0.5, 0.0], [-0.5, 0.0, 0.0],  # 12, 13
                               [-0.5, 0.5, 0.0], [0.0, 1.0, 0.0],  # 14, 15
                               [0.0, -0.5, 0.0]],  # 16
                              ],
        "elements_before": ["O_d", "O_u", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "O_s"],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_2t + CO_b <-> OCO-O_2t + *_b -> O_b + CO2_g + 2*_t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.5, 0.0],  # 1, 2, 3
                               [0.5, -1.5, 0.0], [0.5, -1.0, 0.0],  # 4, 5
                               [0.5, -0.5, 0.0], [0.5, 0.0, 0.0],  # 6, 7
                               [0.5, 0.5, 0.0], [0.0, 0.5, 0.0],  # 8, 9
                               [-0.5, 0.5, 0.0], [-0.5, 0.0, 0.0],  # 10, 11
                               [-0.5, -0.5, 0.0], [-0.5, -1.0, 0.0],  # 12, 13
                               [-0.5, -1.5, 0.0], [0.0, -2.0, 0.0],  # 14, 15
                               [0.0, -0.5, 0.0]],  # 16
                              ],
        "elements_before": ["O_d", "O_u", "C", "V", "V", "V", "V", "V",
                            "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V",
                           "V", "V", "V", "V", "V", "V", "V", "O_s"],
        "basis_sites": [0],
    },

    # O2 dissociative adsorption.
    {
        "reaction": "O2_g + 2*_b -> 2O_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [1.0, 1.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.0, 0.5, 0.0]]
                              ],
        "elements_before": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },
    {
        "reaction": "O2_g + 2*_b -> 2O_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 1.5, 0.0],
                               [1.0, 1.0, 0.0],
                               [0.5, 1.0, 0.0]]
                              ],
        "elements_before": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },

    # CO2_g associative desorption.
    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.0, 0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'C', 'V', 'V', 'O_s'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.0, 0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'C'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [1.0, 1.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.0, 0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'C', 'V', 'V', 'O_s'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [1.0, 1.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.0, 0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'C'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.5, 1.5, 0.0],
                               [1.0, 1.0, 0.0],
                               [0.5, 1.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'C', 'V', 'V', 'O_s'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.5, 1.5, 0.0],
                               [1.0, 1.0, 0.0],
                               [0.5, 1.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'C'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [-1.0, 1.0, 0.0],
                               [-0.5, 1.5, 0.0],
                               [-0.5, 1.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'C', 'V', 'V', 'O_s'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [-1.0, 1.0, 0.0],
                               [-0.5, 1.5, 0.0],
                               [-0.5, 1.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'C'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    # CO2_g associative desorption.
    {
        "reaction": "CO_b + O_b <-> OC-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [1.0, 1.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.0, 0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'C', 'V', 'V', 'V', 'O_s'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_b + O_b <-> OC-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [1.0, 1.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [1.0, 0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'C'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    {
        "reaction": "CO_b + O_b <-> OC-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 1.5, 0.0],
                               [1.0, 1.0, 0.0],
                               [0.5, 1.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'C', 'V', 'V', 'V', 'O_s'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_b + O_b <-> OC-O_2b -> CO2_g + 2*_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 1.5, 0.0],
                               [1.0, 1.0, 0.0],
                               [0.5, 1.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'C'],
        "elements_after": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
    },

    # CO_t + O_b -> CO2_g
    {
        "reaction": "CO_t + O_b <-> CO-O_t + *_b -> CO2_g + *_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [2.0, 0.0, 0.0],
                               [1.5, 0.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [2.0, 0.5, 0.0],
                               [2.5, 0.5, 0.0],
                               [2.5, 0.0, 0.0],
                               [2.5, -0.5, 0.0],
                               [2.0, -0.5, 0.0],
                               [1.5, -0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'C', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_t + O_b <-> CO-O_t + *_b -> CO2_g + *_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [-1.0, 0.0, 0.0],
                               [-1.5, 0.0, 0.0],
                               [-1.5, 0.5, 0.0],
                               [-1.0, 0.5, 0.0],
                               [-0.5, 0.5, 0.0],
                               [-0.5, 0.0, 0.0],
                               [-0.5, -0.5, 0.0],
                               [-1.0, -0.5, 0.0],
                               [-1.5, -0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'C', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_t + O_b <-> CO-O_t + *_b -> CO2_g + *_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.0, 2.0, 0.0],
                               [-0.5, 2.0, 0.0],
                               [-0.5, 2.5, 0.0],
                               [0.0, 2.5, 0.0],
                               [0.5, 2.5, 0.0],
                               [0.5, 2.0, 0.0],
                               [0.5, 1.5, 0.0],
                               [0.0, 1.5, 0.0],
                               [-0.5, 1.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'C', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "basis_sites": [0],
    },
    {
        "reaction": "CO_t + O_b <-> CO-O_t + *_b -> CO2_g + *_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.0, -1.0, 0.0],
                               [-0.5, -1.0, 0.0],
                               [-0.5, -0.5, 0.0],
                               [0.0, -0.5, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, -1.0, 0.0],
                               [0.5, -1.5, 0.0],
                               [0.0, -1.5, 0.0],
                               [-0.5, -1.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'C', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
        "basis_sites": [0],
    },

    # CO diffusion at basis site 0.
    {
        "reaction": "CO_b + *_t <-> CO_t + *_b -> CO_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0], [0.5, 0.0, 0.0]],
                              [[0.0, 0.0, 0.0], [0.0, 0.5, 0.0]],
                              [[0.0, 0.0, 0.0], [-0.5, 0.0, 0.0]],
                              [[0.0, 0.0, 0.0], [0.0, -0.5, 0.0]],
                              ],
        "elements_before": ["C", "V"],
        "elements_after": ["V", "C"],
        "basis_sites": [0],
        "fast": True,
    },

    # O diffusion.
    {
        "reaction": "O_b + *_t <-> O_t + *_b -> O_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0],
                               [1.5, 0.5, 0.0],
                               [2.0, 0.0, 0.0],
                               [1.5, -0.5, 0.0],
                               [1.5, 0.0, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },

    {
        "reaction": "O_b + *_t <-> O_t + *_b -> O_b + *_t",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0],
                               [0.0, -1.0, 0.0],
                               [-0.5, -0.5, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.0, -0.5, 0.0]]
                              ],
        "elements_before": ['V', 'V', 'V', 'V', 'O_s', 'V', 'V', 'V', 'V'],
        "elements_after": ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'O_s'],
        "basis_sites": [0],
    },

    # CO adsorbed at top site.
    {
        "reaction": "CO_g + *_t -> CO_t",
       "coordinates_group": [[[0.0, 0.0, 0.0],
                              [-0.5, 0.0, 0.0],
                              [-0.5, 0.5, 0.0],
                              [0.0, 0.5, 0.0],
                              [0.5, 0.5, 0.0],
                              [0.5, 0.0, 0.0],
                              [0.5, -0.5, 0.0],
                              [0.0, -0.5, 0.0],
                              [-0.5, -0.5, 0.0]]],
        "elements_before": ["V", "V", "V", "V", "V", "V", "V", "V", "V"],
        "elements_after": ["C", "V", "V", "V", "V", "V", "V", "V", "V"],
        "basis_sites": [0],
        "fast": True,
        "redist": True,
        "redist_species": "C",
    },

    # CO adsorbed on bridge site.
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [1.0, 0.0, 0.0],
                               [0.5, -0.5, 0.0],
                               [0.5, 0.0, 0.0]]],
        "elements_before": ["V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "C"],
        "basis_sites": [0],
        "fast": True,
        "redist": True,
        "redist_species": "C",
    },
    {
        "reaction": "CO_g + *_b -> CO_b",
        "coordinates_group": [[[0.0, 0.0, 0.0],
                               [-0.5, 0.5, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.5, 0.5, 0.0],
                               [0.0, 0.5, 0.0]]],
        "elements_before": ["V", "V", "V", "V", "V"],
        "elements_after": ["V", "V", "V", "V", "C"],
        "basis_sites": [0],
        "fast": True,
        "redist": True,
        "redist_species": "C"
    },
]
