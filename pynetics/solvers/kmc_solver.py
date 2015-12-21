import logging
from math import exp

try:
    from KMCLib import *
except ImportError:
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!                                                   !!!"
    print "!!!          WARNING: KMCLib is not installed         !!!"
    print "!!! Any kMC calculation using KMCLib will be disabled !!!"
    print "!!!                                                   !!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

from .. import KineticCoreComponent
from ..errors.error import *
from ..database.thermo_data import kB_eV
from ..database.lattice_data import *
from .. import __version__


class KMCSolver(KineticCoreComponent):
    def __init__(self, owner):
        '''
        Class for kinetic Monte Carlo simulation process.
        '''
        KineticCoreComponent.__init__(self, owner)

        # set logger
        self.logger = logging.getLogger('model.solvers.KMCSolver')

        # scripting header
        self.script_header = (
            '# This file was automatically generated by Pynetix' +
            ' (https://github.com/PytLab/Pynetics).\n' +
            '# Version %s\n#\n' +
            '# Do not make changes to this file ' +
            'unless you know what you are doing\n\n') % __version__

    def get_elementary_rate(self, elementary_rxn_list, force_TST=False):
        '''
        Function to get elementary reaction rate.

        Parameters:
        -----------
        elementary_rxn_list: elementary reaction states list, list of lists of str.

        force_TST: whether force to use TST to get rates, bool

        Returns:
        --------
        Rf: forward rate, float

        Rr: reversed rate, float.

        Example:
        --------
        >>> m.solver.get_elementary_rate([['CO_g', '*_s'], ['CO_s']])
        >>> (2262.3375403296886, 0.022775493982398507)

        '''
        rxn_expression = self.elementary_rxn_list2str(elementary_rxn_list)

        self.logger.info('getting elementary reaction rates for [ %s ]',
                         rxn_expression)
        # check input validity
        try:
            idx = self._owner.elementary_rxns_list.index(elementary_rxn_list)
        except ValueError:
            msg = '%s is not in elementary_rxns_list.' % str(elementary_rxn_list)
            raise ReactionEquationError(msg)

        # forced to use TST
        if force_TST:
            if not ('Ga' and 'dG' in self._owner.relative_energies):
                msg = 'No [ Ga ] and [ dG ] read, check your rel_energy.py please.'
                raise ParameterError(msg)
            # get energy info
            Ga = self._owner.relative_energies['Ga'][idx]
            dG = self._owner.relative_energies['dG'][idx]
            Gar = Ga - dG
            # get forward and reversed rates
            Rf = self.get_reaction_rate(Ga)
            Rr = self.get_reaction_rate(Gar)

        # use corresponding methods
        else:
            # get forward barrier
            Ea = self._owner.relative_energies['Ea'][idx]
            try:
                dE = self._owner.relative_energies['dG'][idx]
                free_energy = True
            except KeyError:
                dE = self._owner.relative_energies['dE'][idx]
                free_energy = False
            # forward rate
            Rf = self.get_forward_rate(elementary_rxn_list, Ea)
            # reversed rate (use dE as nonfree energy change)
            Rr = self.get_reversed_rate(elementary_rxn_list, Ea, dE,
                                        free_energy=free_energy)

        return Rf, Rr

    def check_gas_participating(self, reactants):
        '''
        Check whether gas species is in reactants.

        Parameters:
        -----------
        reactants: reactant species list, list of str.

        Returns:
        --------
        has_gas: gas participating or not, bool
        '''
        gas_name = self.extract_gas_name(reactants)

        if gas_name:
            return True
        else:
            return False

    def extract_gas_name(self, species_list):
        '''
        Extract gas name from a species list.
        '''
        # gas participating or not
        gases = []
        for sp in species_list:
            if sp.endswith('_g'):
                gas_name = self.split_species(sp)[-1]
                gases.append(gas_name)
        # check gas species number
        if len(gases) > 1:
            msg = ('There are more than one gases %s in species_list %s.' %
                   (str(gases), str(species_list)))
            raise ReactionEquationError(msg)
        # get gas name
        if gases:
            gas_name, = gases
        else:
            gas_name = None

        return gas_name

    def get_forward_rate(self, elementary_rxn_list, Ea):
        '''
        Function to determine the reaction type and get forward reaction rate.

        Parameters:
        -----------
        reactants: reactant species list, list of str.

        Ea: elementary reaction enengy barrier, float
        '''
        rxn_expression = self.elementary_rxn_list2str(elementary_rxn_list)

        self.logger.debug('getting forward rate for [ %s ]', rxn_expression)
        reactants = elementary_rxn_list[0]

        gas_name = self.extract_gas_name(reactants)

        if gas_name:
            self.logger.debug('[ %s ] is adsorption process, use Collision Theory.',
                              rxn_expression)
            Rf = self.get_adsorption_rate(gas_name, Ea)
        else:
            self.logger.debug('[ %s ] is not adsorption process, use TST.',
                              rxn_expression)
            Rf = self.get_reaction_rate(Ea)

        self.logger.info('Rf = %.3e', Rf)

        return Rf

    def get_reversed_rate(self, elementary_rxn_list, Ea, dE, free_energy=False):
        '''
        Function to determine the reaction type and get reversed reaction rate.

        Parameters:
        -----------
        elementary_rxn_list: elementary reaction states list, list of lists of str.

        Ea: free energy barrier for forward reaction, float.

        dE: reaction energy change(free energy or not), float.

        free_energy: use dE as a free energy or not, bool.

        Returns:
        --------
        Rr: reversed rate of the elementary reaction, float.

        Example:
        --------
        >>> m.solver.get_reversed_rate([['CO_g', '*_s'], ['CO_s']], 0.0, -1.6)
        >>> 0.022775493982398507

        '''
        rxn_expression = self.elementary_rxn_list2str(elementary_rxn_list)
        self.logger.debug('getting reversed rate for [ %s ]', rxn_expression)

        Ear = Ea - dE  # reversed reaction barrier
        reactants = elementary_rxn_list[0]

        is_desorption = self.check_gas_participating(reactants)
        if is_desorption:
            # use balance condition
            self.logger.debug('[ %s ] is adsorption process, use balance condition.',
                              rxn_expression)
            gas_name = self.extract_gas_name(reactants)
            Rr = self.get_desorption_rate(gas_name, dE, free_energy=free_energy)
        else:
            self.logger.debug('[ %s ] is not adsorption process, reverse reaction equation ' +
                              'and get forward rate of it', rxn_expression)
            reversed_rxn_list = list(reversed(elementary_rxn_list))
            Rr = self.get_forward_rate(reversed_rxn_list, Ear)

        self.logger.info('Rr = %.3e', Rr)

        return Rr

    def get_adsorption_rate(self, gas_name, Ea=0.0):
        '''
        Function to get gas adsorption rate using Collision Theory.

        Parameters:
        -----------
        gas_name: gas molecular formula with suffix, str.

        Ea: energy barrier (not free energy), float.

        Example:
        --------
        >>> m.solver.get_adsorption_rate('CO_g')
        >>> 2262.3375403296886

        '''
        # gas_name without suffix
        stripped_name = gas_name.split('_')[0]
        # parameters for collision theory
        act_ratio = self._owner.active_ratio                       # active area ratio
        Auc = self._owner.unitcell_area                            # unit cell area
        p = self._owner.species_definitions[gas_name]['pressure']  # partial pressure
        m = self._owner.parser.get_molecular_mass(stripped_name, absolute=True)  # molecular mass
        T = self._owner.temperature
        # forward rate
        Rads = self.get_kCT(Ea, Auc, act_ratio, p, m, T)

        return Rads  # s^-1

    def get_desorption_rate(self, gas_name, dE, Ea=0.0, free_energy=False):
        '''
        Function to get desorption in detailed balance condition.

        Parameters:
        -----------
        gas_name: gas molecular formula with suffix, str.

        Ea: energy barrier (not free energy), float.

        dE: correspinding adsorption energy change(E* - E_gas), float.

        free_energy: dE is free energy change or not, False by default, bool.

        Example:
        --------
        >>> m.solver.get_desorption_rate('CO_g', -1.6)
        >>> 0.022775493982398507
        '''
        Rads = self.get_adsorption_rate(gas_name, Ea)

        # gas_name without suffix
        stripped_name = gas_name.split('_')[0]

        T = self._owner.temperature

        if free_energy:
            self.logger.info('free energy read, use it directly.')
            Rdes = Rads/exp(-dE/(kB_eV*T))
        else:
            self.logger.info('NO free energy read, add correction automatically.')
            # get entropy contribution in gas free energy
            delta_miu = self._owner.corrector.entropy_correction(stripped_name)
            self.logger.info('%s entropy correction = %.3e', gas_name, delta_miu)
            K = exp((delta_miu - dE)/(kB_eV*T))  # equilibrum constant
            Rdes = Rads/K

        return Rdes

    def get_reaction_rate(self, Ga):
        '''
        Function to get reaction rate using Transition State Theory.

        Parameters:
        -----------
        Ea: energy barrier (not free energy), float.
        '''
        T = self._owner.temperature
        R = self.get_kTST(Ga, T)

        return R

#--------------------------------------------------------------#
#                KMC Solver class using KMCLib                 #
#--------------------------------------------------------------#


class KMCLibSolver(KMCSolver):
    def __init__(self, owner):
        '''
        Class for kinetic Monte Carlo simulation process using KMCLib.
        '''

        KMCSolver.__init__(self, owner)

        # set logger
        self.logger = logging.getLogger('model.solvers.KMCLibSolver')

    def run(self,
            scripting=True,
            analysis=None,
            trajectory_filename='trajectory.py'):
        '''
        Run the KMC lattice model simulation with specified parameters.

        Parameters:
        -----------
        scripting: generate lattice script or not, True by default, bool.

        analysis: a list of instantiated analysis objects that
                  should be used for on-the-fly analysis, list.

        trajectory_filename: The filename of the trajectory. If not given
                            no trajectory will be saved, str.
        '''
        # get KMCLib KMCControlParameters object
        control_parameters = self.get_control_parameters()
        # get KMCLib KMCLatticeModel object
        model = self.get_lattice_model()

        if scripting:
            self.script_lattice_model('kmc_model.py')
            self.logger.info('script kmc_model.py created.')

        # run KMC main loop
        model.run(control_parameters=control_parameters,
                  trajectory_filename=trajectory_filename,
                  trajectory_type='lattice',
                  analysis=analysis)

    def get_lattice_model(self):
        '''
        Function to get KMCLib KMCLatticeModel object.
        '''
        # KMCLib configuration object
        configuration = self.initialize_configuration()
        # KMCLib interactions object
        interactions = self.get_interactions()
        # KMCLib model object
        model = KMCLatticeModel(configuration, interactions)

        return model

    def initialize_configuration(self):
        '''
        Method to initializing a KMCLib Configuration object.
        '''
        # get lattice unit cell basis
        grid_type = self._owner.grid_type.strip().lower()
        cell_vectors = lattice_cell_vectors[grid_type]

        # basis point of unit cell
        basis_points = [[0.0, 0.0, 0.0]]

        # KMCLib Unitcell instantiation
        unit_cell = KMCUnitCell(cell_vectors=cell_vectors,
                                basis_points=basis_points)

        # KMCLib Lattice instantiation
        repetition = self._owner.grid_shape + (1, )
        pbc = self._owner.pbc
        if pbc:
            periodic = (True, True, False)
        else:
            periodic = (False, False, False)
        lattice = KMCLattice(unit_cell=unit_cell,
                             repetitions=repetition,
                             periodic=periodic)

        # initialize elements types
        nsite = reduce(lambda x, y: x*y, repetition)
        types = ['Vac']*nsite
        adsorbate_names = [ads.split('_')[0] for ads in self._owner.adsorbate_names]
        possible_types = adsorbate_names + ['Vac']

        # KMCLib configuration instantiation
        configuration = KMCConfiguration(lattice=lattice,
                                         types=types,
                                         possible_types=possible_types)

        return configuration

    def get_interactions(self):
        '''
        Function to get KMCLib interactions object.
        '''
        processes = self.get_processes()
        interactions = KMCInteractions(
            processes=processes,
            implicit_wildcards=True)

        return interactions

    def get_control_parameters(self):
        '''
        Function to get KMCLib KMCControlParameters instance.
        '''
        # get parameters in model
        nstep = self._owner.nstep
        dump_interval = self._owner.dump_interval
        seed = self._owner.seed

        # KMCLib control parameter instantiation
        control_parameters = KMCControlParameters(
            number_of_steps=nstep,
            dump_interval=dump_interval,
            seed=seed)

        return control_parameters

    def get_processes(self):
        '''
        Function to get all possible processes in KMC model.

        Returns:
        --------
        processes: list of KMCLib.Processe objects

        '''
        processes = []
        for elementary_rxn_list in self._owner.elementary_rxns_list:
            rxn_expression = self.elementary_rxn_list2str(elementary_rxn_list)
            self.logger.info('-'*56)
            self.logger.info('getting process for [ %s ]', rxn_expression)
            procs = self.get_elementary_processes(elementary_rxn_list)
            processes.extend(procs)

        return processes

    def get_elementary_processes(self, elementary_rxn_list):
        '''
        Function to get KMCLib processes for an elementary reaction.

        Parameters:
        -----------
        elementary_rxn_list: elementary reaction states list, list of lists of str.

        Returns:
        --------
        processes: list of KMCLib.Processe objects

        '''

        # get center site and neighbors coordinates
        coordinates = self.get_coordinates()

        # get rate constants
        kf, kr = self.get_elementary_rate(elementary_rxn_list)

        # get elements changes
        get_elements_changes = self._owner.parser.get_elementary_elements_changes

        def get_single_direction_processes(elementary_rxn_list):
            ''' get single direction process objects '''
            elements_changes = get_elements_changes(elementary_rxn_list)
            processes = []
            for elements_change in elements_changes:
                elements_before, elements_after = elements_change
                self.logger.info('%s -> %s',
                                 str(elements_before),
                                 str(elements_after))
                p = KMCProcess(coordinates=coordinates,
                               elements_before=elements_before,
                               elements_after=elements_after,
                               basis_sites=[0],
                               rate_constant=kf)
                processes.append(p)

            return processes

        # forward direction
        self.logger.info('instantiating forward reaction processes...')
        fprocesses = get_single_direction_processes(elementary_rxn_list)

        # reversed direction
        self.logger.info('instantiating reversed reaction processes...')
        reversed_rxn_list = list(reversed(elementary_rxn_list))
        rprocesses = get_single_direction_processes(reversed_rxn_list)

        processes = fprocesses + rprocesses

        return processes

    def get_coordinates(self):
        ''' get center site and neighbors coordinates '''

        grid_type = self._owner.grid_type
        if grid_type not in grid_neighbor_offsets:
            raise GridTypeError('Unsupported grid type [ %s ]' % grid_type)

        neighbor_offsets = grid_neighbor_offsets[grid_type]
        coordinates = [(0.0, 0.0, 0.0)]
        coordinates.extend(neighbor_offsets)

        return coordinates

    #-----------------------
    # script KMCLib objects |
    #-----------------------

    def script_decorator(func):
        '''
        Decorator for KMCLib objects scripting.
        Add some essential import statements and save operation.
        '''
        def wrapper(self, script_name=None):
            content = self.script_header + 'from KMCLib import *\n\n'
            content += func(self, script_name)

            # write to file
            if script_name:
                script_name = 'auto_' + script_name
                with open(script_name, 'w') as f:
                    f.write(content)
                self.logger.info('interactions script written to %s', script_name)

            return content

        return wrapper

    @script_decorator
    def script_lattice_model(self, script_name=None):
        '''
        Generate a script representation of lattice model instances.

        Parameters:
        -----------
        script_name: filename into which script written, str.
                     set to None by default and no file will be generated.

        Returns:
        --------
        A script that can generate this lattice model object, str.

        '''
        lattice_model = self.get_lattice_model()
        content = lattice_model._script()

        return content

    @script_decorator
    def script_configuration(self, script_name=None):
        '''
        Generate a script representation of interactions instances.

        Parameters:
        -----------
        script_name: filename into which script written, str.
                     set to None by default and no file will be generated.

        Returns:
        --------
        A script that can generate this configuration object, str.

        '''
        configuration = self.initialize_configuration()
        content = configuration._script()

        return content

    @script_decorator
    def script_interactions(self, script_name=None):
        '''
        Generate a script representation of interactions instances.

        Parameters:
        -----------
        script_name: filename into which script written, str.
                     set to None by default and no file will be generated.

        Returns:
        --------
        A script that can generate this interactions object, str.

        '''
        interactions = self.get_interactions()
        content = interactions._script()

        return content

    @script_decorator
    def script_processes(self, script_name=None):
        '''
        Generate a script representation of processes instances.

        Parameters:
        -----------
        script_name: filename into which script written, str.
                     set to None by default and no file will be generated.

        Returns:
        --------
        A script that can generate this process object, str.

        '''
        # get processes objects
        processes = self.get_processes()

        # get content string
        content = ''
        for idx, proc in enumerate(processes):
            proc_str = proc._script('process_%d' % idx)
            content += proc_str
        # gather processes
        proc_str = 'processes = [\n'
        for idx in xrange(len(processes)):
            proc_str += (' '*4 + 'process_%d,\n' % idx)
        proc_str += ']\n\n'

        content += proc_str

        return content
