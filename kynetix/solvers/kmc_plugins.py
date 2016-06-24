import logging

import numpy as np
try:
    from KMCLib import KMCAnalysisPlugin
except ImportError:
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!                                                    !!!"
    print "!!!         WARNING: KMCLibX is not installed          !!!"
    print "!!! Any kMC calculation using KMCLibX will be disabled !!!"
    print "!!!                                                    !!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

try:
    from kynetix.solvers.plugin_backends.kmc_functions import *
except ImportError:
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!   WARNING: plugin backends extension not found.   !!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    from kynetix.solvers.kmc_functions import *

from kynetix import file_header
from kynetix.functions import get_list_string


class CoveragesAnalysis(KMCAnalysisPlugin):
    """
    KMC plugin to do On-The-Fly coverage analysis.
    """
    def __init__(self, kmc_model):
        """
        Constructor of CoverageAnalysis object.

        Parameters:
        -----------
        kmc_model: KMC model object of Kynetix.KineticModel.
        """
        # The ratio of a basis site occupied.
        self.__coverage_ratios = (1.0, 1./2, 1./2, 1./4)

        # Recorder variables.
        self.__times = []
        self.__steps = []
        self.__coverages = []

        self.__possible_types = kmc_model.possible_element_types()
        
        # Set logger.
        self.__logger = logging.getLogger("model.solvers.KMCSolver.CoveragesAnalysis")

    def setup(self, step, time, configuration):
        # Append time and step.
        self.__times.append(time)
        self.__steps.append(step)

        # Collect species coverages.
        types = configuration.types()
        coverages = collect_coverages(types,
                                      self.__possible_types,
                                      self.__coverage_ratios)
        self.__coverages.append(coverages)

    def registerStep(self, step, time, configuration):
        # Do the same thing in setup().
        self.setup(step, time, configuration)

    def finalize(self):
        """
        Write all data to files.
        """
        # Get data strings.
        coverages = zip(*self.__coverages)
        coverages_str = get_list_string("coverages", coverages)
        times_str = get_list_string("times", self.__times)
        steps_str = get_list_string("steps", self.__steps)
        possible_types_str = get_list_string("possible_types", self.__possible_types)

        # Write to file.
        content = file_header + times_str + steps_str + coverages_str + possible_types_str
        filename = "auto_coverages.py"
        with open(filename, "w") as f:
            f.write(content)
        self.__logger.info("coverages informations are written to {}".format(filename))

        return

