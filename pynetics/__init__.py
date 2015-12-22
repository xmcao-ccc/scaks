import cPickle
from math import exp, pi, sqrt

from functions import *
from errors.error import *
from .database.thermo_data import kB_J, kB_eV, kB_eV, h_eV


__version__ = '0.3.0'

#-------------------------------------------------------
# Some base classes for kinetic model are defined below |
#-------------------------------------------------------


class ModelShell(object):
    '''
    A non-functional parent class to be inherited by
    other tools class of kinetic model.
    '''

    def __init__(self, owner):
        self._owner = owner
        self.archived_data_dict = {}

    def split_species(self, species_str):
        '''
        Split species_str to number(int) and species_name(str)

        Parameters:
        -----------
        species_str: species string, e.g. '2CH4_g', str
        '''
        # for species adsorbated on surface
        if not '*' in species_str:
            m = self._owner.regex_dict['species'][0].search(species_str)

            # check successful match or not
            if not m:
                msg = 'Unsuccessful spit for species: %s' % species_str
                raise SpeciesError(msg)

            if not m.group(1):
                stoichiometry = 1
            else:
                stoichiometry = int(m.group(1))
            species_name = m.group(2) + '_' + m.group(3) + m.group(4)
            return stoichiometry, species_name

        # for site
        else:
            m = self._owner.regex_dict['empty_site'][0].search(species_str)
            if not m.group(1):
                stoichiometry = 1
            else:
                stoichiometry = int(m.group(1))
            site_name = '*_' + m.group(2)
            return stoichiometry, site_name

    def update_defaults(self, defaults):
        '''
        Update values in defaults dict,
        if there are custom parameters in setup file.

        Parameters:
        -----------
        default: default attributes dict, dict.
        '''

        for parameter_name in defaults:
            if hasattr(self._owner, parameter_name):
                defaults[parameter_name] = \
                    getattr(self._owner, parameter_name)

        return defaults

    def archive_data(self, data_name, data):
        '''
        Update data dict and dump it to data file.

        Parameters:
        -----------
        data_name: key in data dict, str.

        data: value in data dict, any python data type.
        '''

        #update data dict
        if data_name in self.archived_variables:
            self.archived_data_dict[data_name] = data
            #dump data dict to data file
            if self.archived_data_dict:
                with open(self._owner.data_file, 'wb') as f:
                    cPickle.dump(self.archived_data_dict, f)

    def elementary_rxn_list2str(self, elementary_rxn_list):
        '''
        Convert elementary_rxn_list to rxn_expression.
        '''
#        try:
#            idx = self._owner.elementary_rxns_list.index(elementary_rxn_list)
#        except ValueError:
#            raise ReactionEquationError('%s is not in elementary_rxns_list' %
#                                        str(elementary_rxn_list))
#        rxn_expression = self._owner.rxn_expressions[idx]

        def state2str(state):
            return ' + '.join(state)

        state_strs = []
        for state in elementary_rxn_list:
            state_str = state2str(state)
            state_strs.append(state_str)

        if len(state_strs) == 3:
            IS, TS, FS = state_strs
            rxn_expression = IS + ' <-> ' + TS + ' -> ' + FS
        elif len(state_strs) == 2:
            IS, FS = state_strs
            rxn_expression = IS + ' -> ' + FS

        return rxn_expression

    @staticmethod
    def write2file(filename, line):
        f = open(filename, 'a')
        f.write(line)
        f.close()


class KineticCoreComponent(ModelShell):
    '''
    Base class to be herited by core components of micro kinetic model,
    e.g. solver, simulator...
    '''

    def __init__(self, owner):
        ModelShell.__init__(self, owner)

    @staticmethod
    def get_kTST(Ga, T):
        '''
        Function to get rate constants according to Transition State Theory.

        Parameters:
        -----------
        Ga: free energy barrier, float.

        T: thermodynamics constants, floats.
        '''

        kTST = kB_eV*T/h_eV*exp(-Ga/(kB_eV*T))

        return kTST

    @staticmethod
    def get_kCT(Ea, Auc, act_ratio, p, m, T, f=1.0):
        '''
        Function to get rate constant/collision rate according to Collision Theory.

        Parameters:
        -----------
        Ea: energy barrier( NOT free energy barrier), float.

        Auc: area of unitcell (m^-2), float.

        act_ratio: area of active sites/area of unitcell, float(<= 1.0).

        p: partial pressure of gas, float.

        m: absolute mass of molecule (kg), float.

        f: factor accounts for a further reduction in the sticking probability,
           if particle with certain initial states are not efficiently steered
           along the MEP, and reflected by a higher barrier, float(<= 1.0).

        T: temperature (K), float.
        '''
        # check parameters
        if act_ratio > 1.0:
            msg = 'active area ratio must be less than 1.0'
            raise ParameterError(msg)
        if f > 1.0:
            msg = 'factor f must be less than 1.0'
            raise ParameterError(msg)

        S = f*act_ratio*exp(-Ea/(kB_eV*T))      # sticking coefficient
        kCT = S*(p*Auc)/(sqrt(2*pi*m*kB_J*T))  # rate

        return kCT
