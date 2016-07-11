from copy import deepcopy
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
from kynetix.utilities.format_utilities import get_list_string, get_dict_string


class CoveragesAnalysis(KMCAnalysisPlugin):
    """
    KMC plugin to do On-The-Fly coverage analysis.
    """
    # {{{
    def __init__(self, kmc_model, filename="auto_coverages.py"):
        """
        Constructor of CoverageAnalysis object.

        Parameters:
        -----------
        kmc_model: KMC model object of Kynetix.KineticModel.
        """
        # LatticeModel object.
        self.__kmc_model = kmc_model

        # Recorder variables.
        self.__times = []
        self.__steps = []
        self.__coverages = []

        self.__possible_types = kmc_model.possible_element_types()

        # Set logger.
        self.__logger = logging.getLogger("model.solvers.KMCSolver.CoveragesAnalysis")

        # Set data file name.
        self.__filename = filename

    def setup(self, step, time, configuration, interactions):
        # Append time and step.
        self.__times.append(time)
        self.__steps.append(step)

        # Collect species coverages.
        types = configuration.types()
        coverages = collect_coverages(types, self.__possible_types)

        self.__coverages.append(coverages)

    def registerStep(self, step, time, configuration, interactions):
        # Do the same thing in setup().
        self.setup(step, time, configuration, interactions)

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
        with open(self.__filename, "w") as f:
            f.write(content)

        # Info output.
        msg = "coverages informations are written to {}".format(self.__filename)
        self.__logger.info(msg)

        return
        # }}}


class FrequencyAnalysis(KMCAnalysisPlugin):
    """
    KMC plugin to do On-The-Fly process occurence frequency analysis.
    """
    # {{{
    def __init__(self,
                 kmc_model,
                 filename="auto_frequency.py",
                 buffer_size=500,
                 tof_start=0):
        """
        Constructor of TOFAnalysis object.

        Parameters:
        -----------
        kmc_model: KMC model object of Kynetix.KineticModel.

        filename: The name of data file, str.

        buffer_size: The max length of recorder variables.
        """
        # LatticeModel object.
        self.__kmc_model = kmc_model

        # Recorder variables.
        self.__times = []
        self.__steps = []

        # Process indices.
        self.__picked_indices = []

        # Process pick statistics list.
        nprocess = len(kmc_model.processes())
        self.__process_occurencies = [0]*nprocess
        self.__steady_process_occurencies = [0]*nprocess

        # Set logger.
        self.__logger = logging.getLogger("model.solvers.KMCSolver.FrequencyAnalysis")

        # Max length of recorder variables.
        self.__buffer_size = buffer_size

        # TOF start step.
        self.__tof_start_time = 0.0
        self.__tof_end_time = 0.0

        # Name of data file.
        self.__filename = filename

    def setup(self, step, time, configuration, interactions):
        # Append time and step.
#        self.__times.append(time)
#        self.__steps.append(step)
#
#        # Flush counter.
#        self.__flush_counter = 0
#
#        # Create statistic data file.
        variables_str = ("times = []\nsteps = []\npicked_indices = []\n" +
                         "process_occurencies = []\n")
        with open(self.__filename, "w") as f:
            content = file_header + variables_str
            f.write(content)

    def registerStep(self, step, time, configuration, interactions):
        # Append time and step.
#        self.__times.append(time)
#        self.__steps.append(step)

        # Append picked index.
        picked_index = interactions.pickedIndex()
        self.__picked_indices.append(picked_index)

        # Add to collection list.
        self.__process_occurencies[picked_index] += 1

        # Collect steady frequency info.
        if step >= self.__kmc_model.tof_start():
            self.__steady_process_occurencies[picked_index] += 1

            if not self.__tof_start_time:
                self.__tof_start_time = time
                self.__logger.info("TOF analysis start at time = {:f}".format(time))

        self.__tof_end_time = time

#        # Check and flush.
#        if len(self.__picked_indices) >= self.__buffer_size:
#            self.__flush()

    def finalize(self):
        """
        Write all data to files.
        """
        # Flush data left to file.
#        self.__flush()

        # Write process occurencies to file.
        occurencies_str = get_list_string("process_occurencies",
                                          self.__process_occurencies)

        # Calculate reaction occurencies.
        process_mapping = self.__kmc_model.process_mapping()

        # Construct reaction occurencies dict.
        reaction_occurencies = {}
        steady_reaction_occurencies = {}

        for reaction in set(process_mapping):
            reaction_occurencies.setdefault(reaction, 0)
            steady_reaction_occurencies.setdefault(reaction, 0)

        # Fill the dict.
        for occurency, reaction in zip(self.__process_occurencies, process_mapping):
            reaction_occurencies[reaction] += occurency

        for occurency, reaction in zip(self.__steady_process_occurencies, process_mapping):
            steady_reaction_occurencies[reaction] += occurency

        reaction_occurencies_str = get_dict_string("reaction_occurencies",
                                                   reaction_occurencies)
        steady_reaction_occurencies_str = get_dict_string("steady_reaction_occurencies",
                                                          steady_reaction_occurencies)

        # Calculate rates.
        delta_t = self.__tof_end_time - self.__tof_start_time
        reaction_rates = {}
        for reaction, occurency in steady_reaction_occurencies.iteritems():
            rate = occurency/delta_t
            reaction_rates.setdefault(reaction, rate)
        reaction_rates_str = get_dict_string("reaction_rates", reaction_rates)

        with open(self.__filename, "a") as f:
            all_content = (occurencies_str + reaction_occurencies_str +
                           steady_reaction_occurencies_str + reaction_rates_str)
            f.write(all_content)

        # Info output.
        msg = "frequency informations are written to {}".format(self.__filename)
        self.__logger.info(msg)

    def __flush(self):
        """
        Private function to flush data in buffer.
        """
        # Get picked index extension strings.
        var_name = "picked_indices_{}".format(self.__flush_counter)
        list_str = get_list_string(var_name, self.__picked_indices, ncols=40)
        extend_str = "picked_indices.extend({})\n\n".format(var_name)
        picked_indices_str = list_str + extend_str

        # Get times extension strings.
        var_name = "times_{}".format(self.__flush_counter)
        list_str = get_list_string(var_name, self.__times)
        extend_str = "times.extend({})\n\n".format(var_name)
        times_str = list_str + extend_str

        # Get steps extension strings.
        var_name = "steps_{}".format(self.__flush_counter)
        list_str = get_list_string(var_name, self.__steps, ncols=10)
        extend_str = "steps.extend({})\n\n".format(var_name)
        steps_str = list_str + extend_str

        # Get all content to be flushed.
        comment = ("\n# -------------------- flush {} " +
                   "---------------------\n").format(self.__flush_counter)
        content = comment + times_str + steps_str + picked_indices_str

        # Flush to file.
        with open(self.__filename, "a") as f:
            f.write(content)

        # Free buffers.
        self.__picked_indices = []
        self.__steps = []
        self.__times = []

        self.__flush_counter += 1

    # }}}


#class TOFAnalysis(KMCAnalysisPlugin):
#    """
#    KMC plugin to do On-The-Fly turnover frequency analysis.
#    """
#    def __init__(self,
#                 kmc_model,
#                 filename="auto_tof.py"):
#        """
#        Constructor of TOFAnalysis object.
#
#        Parameters:
#        -----------
#        kmc_model: KMC model object of Kynetix.KineticModel.
#
#        filename: The name of data file, str.
#
#        buffer_size: The max length of recorder variables.
#        """
#        # LatticeModel object.
#        self.__kmc_model = kmc_model
#
#        # Recorder variables.
#        self.__times = []
#        self.__steps = []
#
#        # Process total available site.
#        self.__process_available_sites = []
#
#        # Set logger.
#        self.__logger = logging.getLogger("model.solvers.KMCSolver.TOFAnalysis")
#
#        # Name of data file.
#        self.__filename = filename
#
#    def setup(self, step, time, configuration, interactions):
#        # Append time and step.
#        self.__times.append(time)
#        self.__steps.append(step)
#
#        available_sites = interactions.processAvailableSites()
#        self.__process_available_sites.append(available_sites)
#
#    def registerStep(self, step, time, configuration, interactions):
#        self.setup(step, time, configuration, interactions)
#
#    def finalize(self):
#        times_str = get_list_string("times", self.__times)
#        steps_str = get_list_string("steps", self.__steps)
#        available_sites_str = get_list_string("process_available_sites",
#                                              self.__process_available_sites, 1)
#        
#        content = file_header + times_str + steps_str + available_sites_str
#        with open(self.__filename, "w") as f:
#            f.write(content)
#
#        # Info output.
#        msg = "TOF informations are written to {}".format(self.__filename)
#        self.__logger.info(msg)
#
#        return
