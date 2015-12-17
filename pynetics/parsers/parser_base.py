import copy

import numpy as np

from pynetics import ModelShell
from pynetics.functions import *


class ParserBase(ModelShell):
    '''
    class to operate and analyse rxn equations and rxn lists.
    '''
    def __init__(self, owner):
        """
        A class acts as a base class to be inherited by other
        parser classes, it is not functional on its own.
        """
        ModelShell.__init__(self, owner)

    def check_conservation(self, states_dict):
        """
        Expect a state dict generated by parse_single_elementary_rxn(),
        check mass conservation for a single equation.
        """
        if not states_dict['TS']:
            states_list = ['IS', 'FS']
            state_elements_list = []
            state_site_list = []
            for state in states_list:
                #get element dict
                elements_sum_dict = \
                    self.get_elements_num_dict(states_dict[state]['species_dict'])
                state_elements_list.append(elements_sum_dict)
                #get site dict
                total_site_dict = self.get_total_site_dict(states_dict[state])
                state_site_list.append(total_site_dict)

            if state_elements_list[0] != state_elements_list[1]:
                return 'mass_nonconservative'
            if state_site_list[0] != state_site_list[1]:
                return 'site_nonconservative'
        else:
            states_list = ['IS', 'TS', 'FS']
            state_elements_list = []
            state_site_list = []
            for state in states_list:
                #get element dict
                elements_sum_dict = \
                    self.get_elements_num_dict(states_dict[state]['species_dict'])
                state_elements_list.append(elements_sum_dict)
                #get site dict
                total_site_dict = self.get_total_site_dict(states_dict[state])
                state_site_list.append(total_site_dict)

            if not(state_elements_list[0] == state_elements_list[1] ==
                    state_elements_list[2]):
                return 'mass_nonconservative'
            if not(state_site_list[0] == state_site_list[1] ==
                    state_site_list[2]):
                return 'site_nonconservative'

    def get_total_site_dict(self, state_dict):
        """
        Expect a state_dict(not states_dict as above), e.g.
        {'empty_sites_dict': {'s': {'number': 1, 'type': 's'},
         'species_dict': {'CH-H_s': {'elements': {'C': 1, 'H': 2},
                          'number': 1,
                          'site': 's'}},
         'state_expression': 'CH-H_s + *_s'}

         Return a total site dict, e.g. {'s': 2}
        """
        total_site_dict = {}
        if state_dict['empty_sites_dict']:
            for empty_site in state_dict['empty_sites_dict']:
                total_site_dict.setdefault(
                    empty_site,
                    state_dict['empty_sites_dict'][empty_site]['number']
                )

        #get site number from species dict
        for species in state_dict['species_dict']:
            site = state_dict['species_dict'][species]['site']
            if site == 'g' or site == 'l':  # neglect gas site and liquid site when check conservation
                continue
            site_number = state_dict['species_dict'][species]['site_number']
            sp_number = state_dict['species_dict'][species]['number']
            if site in total_site_dict:
                total_site_dict[site] += sp_number*site_number
            else:
                total_site_dict.setdefault(site, sp_number*site_number)
        return total_site_dict

    def get_elements_num_dict(self, species_dict):
        """
        Expect a species_dict for a state, e.g.
        {'C_s': {'elements': {'C': 1}, 'number': 1, 'site': 's'},
         'CO_s': {'elements': {'C': 1, 'O': 1}, 'number': 2, 'site': 's'}}
        sum all element number, and return a dict, e.g.
        {'C': 2, 'O': 1}
        """
        sum_element_dict = {}
        for sp in species_dict:
            sp_num = species_dict[sp]['number']
            group = {}
            #generate a dict e.g. group = {'C': 2, 'O': 2}
            for element in species_dict[sp]['elements']:
                group.setdefault(element,
                                 species_dict[sp]['elements'][element]*sp_num)
            sum_element_dict = \
                self.merge_elements_dict(sum_element_dict, group)

        return sum_element_dict

    @staticmethod
    def merge_elements_dict(dict_1, dict_2):
        """
        Merge 2 elements_dict. Add dict_2 to dict_1.
        """
        for element in dict_2:
            if element in dict_1:
                dict_1[element] = dict_1[element] + dict_2[element]
            else:
                dict_1[element] = dict_2[element]

        return dict_1

    def parse_elementary_rxns(self, elementary_rxns):
        """
        Parse all elementary rxn equations by analyse states_dict,
        set attrs e.g. elementary_rxns_list, adsorbate_names, gas_names...
        as attrs of model instance.
        """
        elementary_rxns_list = []
        adsorbate_names = []
        gas_names = []
        liquid_names = []
        site_names = []
        transition_state_names = []

        for equation in self._owner.rxn_expressions:
            # debug info
            self.logger.debug('parsing [ %s ]', equation)

            states_dict, elementary_rxn = \
                self.parse_single_elementary_rxn(equation)
            #check conservation firstly
            check_result = self.check_conservation(states_dict)
            if check_result == 'mass_nonconservative':
                raise ValueError('Mass of chemical equation \''+equation +
                                 '\' is not conservative!')
            if check_result == 'site_nonconservative':
                raise ValueError('Site of chemical equation \''+equation +
                                 '\' is not conservative!')
            #analyse state_dict
            for state in states_dict:
                if not states_dict.get(state):
                    continue
                #for transition state, get ts names in addition
                #NOTE: maybe like this -> 'TS': {}
                if state == 'TS' and states_dict.get('TS'):  # ??? need to check '-'?
                    transition_state_names += \
                        states_dict[state]['species_dict'].keys()
                #collect site names
                if states_dict[state].get('empty_sites_dict', None):
                    site_names += states_dict[state]['empty_sites_dict'].keys()
                #collect gas names and adsorbate names
                for sp in states_dict[state]['species_dict']:
                    if states_dict[state]['species_dict'][sp]['site'] == 'g':  # sp is gas
                        gas_names.append(sp)
                    elif states_dict[state]['species_dict'][sp]['site'] == 'l':  # sp is in liquid
                        liquid_names.append(sp)
                    elif not '-' in sp:  # sp is adsorbate
                        adsorbate_names.append(sp)
            #merge elementary rxn
            elementary_rxns_list.append(elementary_rxn)
        #merge duplicates in lists
        self._owner.adsorbate_names = tuple(sorted(list(set(adsorbate_names))))
        self._owner.gas_names = tuple(sorted(list(set(gas_names))))
        self._owner.liquid_names = tuple(sorted(list(set(liquid_names))))
        self._owner.site_names = tuple(sorted(list(set(site_names))))
        self._owner.transition_state_names = \
            tuple(sorted(list(set(transition_state_names))))
        self._owner.elementary_rxns_list = elementary_rxns_list
        #return adsorbate_names, gas_names, site_names, transition_state_names

    def parse_single_elementary_rxn(self, equation):
        """
        Parse single rxn equation,
        return states dicts of states expressions, like
        states_dict =
        {'TS': {state_expression: 'H-O_s + *_s', 'species_dict': {...}},
         'IS': {}}
        and elementary_rxn(list), e.g. [['HCOOH_g', '*_s'], ['HCOOH_s']]
        """
        elementary_rxn = []

        # begin to parse single equation

        # extract IS, TS, FS expressions
        states_dict = {'IS': {}, 'TS': {}, 'FS': {}}
        m = self._owner.regex_dict['IS_TS_FS'][0].search(equation)

        for state in self._owner.regex_dict['IS_TS_FS'][1]:
            idx = self._owner.regex_dict['IS_TS_FS'][1].index(state)
            if m.group(idx+1):
                states_dict[state]['state_expression'] = m.group(idx+1).strip()
                #analyse state expression
                state_expression = states_dict[state]['state_expression']
                species_dict, empty_sites_dict, state_species_list = \
                    self.parse_state_expression(state_expression)
                states_dict[state]['species_dict'] = species_dict
                states_dict[state]['empty_sites_dict'] = empty_sites_dict
                elementary_rxn.append(state_species_list)

        return states_dict, elementary_rxn

    def parse_state_expression(self, state_expression):
        """
        Parse in state_expression in elementary equation,
        e.g. 'HCOOH_g + *_s'.

        Return species_dict, empty_sites_dict and species_list, like
        {'sp_dict': {'CH-H_s': {'number': 1,
                              'site': 's',
                              'elements': {'C': 1, 'H': 2}}}},
        {'s': {'number': 1, 'type': 's'}},
        ['CH2-H_s', '*_s']
        """
        state_dict = {}
        merged_species_list = []
        species_dict, empty_sites_dict = {}, {}
        state_dict['state_expression'] = state_expression
        if '+' in state_expression:
            species_list = state_expression.split('+')
            #strip whitespace in sp_name
            species_list = [raw_sp.strip() for raw_sp in species_list]

            #merge repetitive sp in species_list
            sp_num_dict = {}
            for sp_str in species_list:
                stoichiometry, raw_sp_name = self.split_species(sp_str)
                if raw_sp_name not in sp_num_dict:
                    sp_num_dict.setdefault(raw_sp_name, stoichiometry)
                else:
                    sp_num_dict[raw_sp_name] += stoichiometry
            #convert dict to new merged species_list
            for raw_sp_name in sp_num_dict:
                if sp_num_dict[raw_sp_name] == 1:
                    merged_sp_name = raw_sp_name
                else:
                    merged_sp_name = str(sp_num_dict[raw_sp_name]) + raw_sp_name
                merged_species_list.append(merged_sp_name)
            #Ok! we get a new merged species list

            for sp in merged_species_list:
#                sp = sp.strip()
#                clean_species_list.append(sp)
                if not '*' in sp:
                    species_dict.update(self.parse_species_expression(sp))
                else:
                    empty_sites_dict.update(self.parse_site_expression(sp))
        else:
            sp = state_expression.strip()
            merged_species_list.append(sp)
            if not '*' in sp:
                species_dict.update(self.parse_species_expression(sp))
            else:
                empty_sites_dict.update(self.parse_site_expression(sp))

        return species_dict, empty_sites_dict, merged_species_list

    def parse_species_expression(self, species_expression):
        """
        Parse in species expression like '2CH3_s',
        return a sp_dict like
        {'CH3_s': {'number': 2, 'site': 's', 'elements': {'C': 1, 'H':3}}}
        """
        m = self._owner.regex_dict['species'][0].search(species_expression)
        #['stoichiometry','name','site']
        if m.group(1):
            stoichiometry = int(m.group(1))
        else:
            stoichiometry = 1
        species_name = m.group(2)
        if m.group(3):
            site_number = int(m.group(3))
        else:
            site_number = 1
        site = m.group(4)
        if site_number == 1:
            total_name = species_name + '_' + site
        else:
            total_name = species_name + '_' + str(site_number) + site
        #analyse elements
        if '-' in species_name:
            species_name = species_name.replace('-', '')
        elements_list = string2symbols(species_name)
        elements_type_list = list(set(elements_list))
        elements_dict = {}
        for element in elements_type_list:
            elements_dict.setdefault(element,  # ha, is this pythonic?
                                     elements_list.count(element))
        #create sp_dict
        sp_dict = {}
        sp_dict[total_name] = {
            'number': stoichiometry,
            'site': site,
            'site_number': site_number,
            'elements': elements_dict}

        #below is species_definition part
        #add species to self.species_defination
        if not total_name in self._owner.species_definitions:
            self._owner.species_definitions[total_name] = \
                sp_dict[total_name].copy()
            del self._owner.species_definitions[total_name]['number']
        else:
            self._owner.species_definitions[total_name].update(sp_dict[total_name])
            del self._owner.species_definitions[total_name]['number']
#        self._owner.species_definitions[total_name]['name'] = species_name
        self._owner.species_definitions[total_name]['name'] = m.group(2)
        #add species type to species_definition
        if site != 'g' and site != 'l':
            if '-' in total_name:
                self._owner.species_definitions[total_name]['type'] = 'transition_state'
            else:
                self._owner.species_definitions[total_name]['type'] = 'adsorbate'
        elif site == 'g':
            self._owner.species_definitions[total_name]['type'] = 'gas'
        elif site == 'l':
            self._owner.species_definitions[total_name]['type'] = 'liquid'
        #part end
        return sp_dict

    def parse_site_expression(self, site_expression):
        """
        Parse in species expression like '2*_s',
        return a empty_sites_dict like,
        {'s': 'number': 2, 'type': 's'}
        """
        m = self._owner.regex_dict['empty_site'][0].search(site_expression)
        #['stoichiometry', 'site']
        if m.group(1):
            stoichiometry = int(m.group(1))
        else:
            stoichiometry = 1
        site = m.group(2)
        #create site dict
        empty_sites_dict = {}
        empty_sites_dict[site] = {'number': stoichiometry, 'type': site}
        return empty_sites_dict

    def get_stoichiometry_matrices(self):
        """
        Go through elementary_rxns_list, return sites stoichiometry matrix,
        reactants and products stoichiometry matrix.
        """
        sites_names = ['*_'+site_name for site_name in self._owner.site_names] + \
            list(self._owner.adsorbate_names)
        #reactant and product names
        reapro_names = list(self._owner.gas_names + self._owner.liquid_names)
        #initialize matrices
        m = len(self._owner.elementary_rxns_list)
        n_s, n_g = len(sites_names), len(reapro_names)
        site_matrix, reapro_matrix = np.matrix(np.zeros((m, n_s))),\
            np.matrix(np.zeros((m, n_g)))
        #go through all elementary equations
        for i in xrange(m):
            states_list = self._owner.elementary_rxns_list[i]
            for sp in states_list[0]:  # for initial state
                stoichiometry, sp_name = self.split_species(sp)
                if sp_name in sites_names:
                    j = sites_names.index(sp_name)
                    site_matrix[i, j] += stoichiometry
                if sp_name in reapro_names:
                    j = reapro_names.index(sp_name)
                    reapro_matrix[i, j] += stoichiometry
            for sp in states_list[-1]:  # for final state
                stoichiometry, sp_name = self.split_species(sp)
                if sp_name in sites_names:
                    j = sites_names.index(sp_name)
                    site_matrix[i, j] -= stoichiometry
                if sp_name in reapro_names:
                    j = reapro_names.index(sp_name)
                    reapro_matrix[i, j] -= stoichiometry
        setattr(self._owner, 'reapro_matrix', reapro_matrix)
        setattr(self._owner, 'site_matrix', site_matrix)

        return site_matrix, reapro_matrix

    def get_total_rxn_equation(self):
        "Get total reaction expression of the kinetic model."
        site_matrix, reapro_matrix = self.get_stoichiometry_matrices()

        def null(A, eps=1e-10):
            "get null space of transposition of site_matrix"
            u, s, vh = np.linalg.svd(A, full_matrices=1, compute_uv=1)
            null_space = np.compress(s <= eps, vh, axis=0)
            return null_space.T
#        def null(A, eps=1e-15):
#            u, s, vh = scipy.linalg.svd(A)
#            null_mask = (s <= eps)
#            null_space = scipy.compress(null_mask, vh, axis=0)
#            return scipy.transpose(null_space)
        x = null(site_matrix.T)  # basis of null space
        if not x.any():  # x is not empty
            raise ValueError('Failed to get basis of nullspace.')
        x = map(abs, x.T.tolist()[0])
        #convert entries of x to integer
        min_x = min(x)
        x = [round(i/min_x, 1) for i in x]
        setattr(self._owner, 'trim_coeffients', x)
        x = np.matrix(x)
        total_coefficients = (x*reapro_matrix).tolist()[0]
#        print total_coefficients
        #cope with small differences between coeffs
        abs_total_coefficients = map(abs, total_coefficients)
        min_coeff = min(abs_total_coefficients)
        total_coefficients = [int(i/min_coeff) for i in total_coefficients]
#        print total_coefficients
        #create total rxn expression
        reactants_list, products_list = [], []
        reapro_names = self._owner.gas_names + self._owner.liquid_names
        for sp_name in reapro_names:
            idx = reapro_names.index(sp_name)
            coefficient = total_coefficients[idx]
            if coefficient < 0:  # for products
                coefficient = abs(int(coefficient))
                if coefficient == 1:
                    coefficient = ''
                else:
                    coefficient = str(coefficient)
                products_list.append(coefficient + sp_name)
            else:  # for reactants
                coefficient = int(coefficient)
                if coefficient == 1:
                    coefficient = ''
                else:
                    coefficient = str(coefficient)
                reactants_list.append(coefficient + sp_name)
        #get total rxn list and set it as an attr of model
        total_rxn_list = [reactants_list, products_list]
        self._owner.total_rxn_list = total_rxn_list
        reactants_expr = ' + '.join(reactants_list)
        products_expr = ' + '.join(products_list)
        total_rxn_equation = reactants_expr + ' -> ' + products_expr
#        print total_rxn_equation

        #check conservation
        states_dict = self.parse_single_elementary_rxn(total_rxn_equation)[0]
        check_result = self.check_conservation(states_dict)
        if not check_result:
            setattr(self._owner, 'total_rxn_equation', total_rxn_equation)
        else:
            if check_result == 'mass_nonconservative':
                raise ValueError('Mass of total equation \'' +
                                 total_rxn_equation+'\' is not conservative!')
            if check_result == 'site_nonconservative':
                raise ValueError('Site of total equation \'' +
                                 total_rxn_equation+'\' is not conservative!')

        return total_rxn_equation

    #below 3 methods are used to merge elementary_rxn_lists
    #note: there is no reaction equation balancing operations(may add later, if need)
    def get_end_sp_list(self):
        #get sp list and set it as an attr of the model
        end_sp_list = []
        #add site strings
        for site_name in self._owner.site_names:
            site_str = '*_' + site_name
            end_sp_list.append(site_str)
        #add gas names
        end_sp_list.extend(self._owner.gas_names)
        #add adsorbate names
        end_sp_list.extend(self._owner.adsorbate_names)
        self._owner.end_sp_list = end_sp_list

        return end_sp_list

    def get_coefficients_vector(self, elementary_rxn_list):
        """
        Expect a elementary_rxn_list e.g.
        [['HCOOH_s', '*_s'], ['H-COOH_s', '*_s'], ['COOH_s', 'H_s']],
        return corresponding coefficients vector, e.g.
        [1, 0, 0, 0, 0, -1, 1, -1]
        """
        if not hasattr(self._owner, 'end_sp_list'):
            self.get_end_sp_list()
        end_sp_list = self._owner.end_sp_list

        #intialize coefficients vector
        coeff_list = [0]*len(end_sp_list)
        ends_states = (elementary_rxn_list[0], elementary_rxn_list[-1])
        for state_idx, state_list in enumerate(ends_states):
            for sp_str in state_list:
                stoichiometry, species_name = self.split_species(sp_str)
                coeff_idx = end_sp_list.index(species_name)
                if state_idx == 0:
                    coeff = stoichiometry
                else:
                    coeff = -stoichiometry
                #replace corresponding 0 by coeff
                coeff_list[coeff_idx] = coeff

        return np.array(coeff_list)

    def merge_elementary_rxn_list(self, *lists):
        """
        Expect 2 elementary_rxn_list, e.g.
        [['HCOOH_s', '*_s'], ['H-COOH_s', '*_s'], ['COOH_s', 'H_s']]
        and
        [['*_s', 'COOH_s'], ['*_s', 'COO-H_s'], ['CO2_s', 'H_s']],
        return a merged elementary_rxn_list, e.g.
        [['2*_s', 'HCOOH_s'], ['CO2_s', '2H_s']]
        """
        if not hasattr(self._owner, 'end_sp_list'):
            self.get_end_sp_list()
        end_sp_list = self._owner.end_sp_list

        vect_len = len(end_sp_list)
        merged_vect = np.zeros(vect_len)

        for elementary_rxn_list in lists:
            coeff_vect = self.get_coefficients_vector(elementary_rxn_list)
            merged_vect += coeff_vect

        #go through merged_vect to get merged elementary_rxn_list
        left_list, right_list = [], []
        for coeff, sp_name in zip(merged_vect, end_sp_list):
            if coeff > 0:
                if coeff == 1:
                    sp_str = sp_name
                else:
                    sp_str = str(int(coeff)) + sp_name
                left_list.append(sp_str)
            elif coeff < 0:
                coeff = abs(coeff)
                if coeff == 1:
                    sp_str = sp_name
                else:
                    sp_str = str(int(coeff)) + sp_name
                right_list.append(sp_str)

        merged_elementary_rxn_list = [left_list, right_list]

        return merged_elementary_rxn_list

    #methods below are used to find original gas specie of an intermediate
    @staticmethod
    def remove_site_str(state_list):
        """
        Expect a state list e.g. ['2*_s', 'H2O_g'],
        remove site str in it,
        return a new list, e.g. [H2O_g']
        """
        state_list_copy = copy.copy(state_list)
        for sp_str in state_list_copy:
            if '*' in sp_str:
                state_list_copy.remove(sp_str)
        return state_list_copy

    def strip_sp_list(self, sp_list):
        "Remove stoichiometry of species in sp_list."
        striped_sp_list = []
        for sp_str in sp_list:
            stoichiometry, sp_name = self.split_species(sp_str)
            striped_sp_list.append(sp_name)

        return striped_sp_list

    def find_parent_species(self, sp_name):
        """
        Expect a rxns_list e.g.
        [[['*_s', 'HCOOH_g'], ['HCOOH_s']],
        [['HCOOH_s', '*_s'], ['*_s', 'HCO-OH_s'], ['HCO_s', 'OH_s']],
        [['HCO_s', '*_s'], ['*_s', 'H-CO_s'], ['CO_s', 'H_s']],
        [['H_s', 'OH_s'], ['H-OH_s', '*_s'], ['2*_s', 'H2O_g']],
        [['CO_s'], ['CO-_s'], ['*_s', 'CO_g']],
        [['H2O_s'], ['*_s', 'H2O_g']]],
        and a species name, e.g. 'H_s',
        return a list of its parent species, e.g. ['HCO_s']
        """
        parent_list = []
        rxns_list = self._owner.elementary_rxns_list
        for rxn_list in rxns_list:
            FS_sp_list = self.strip_sp_list(rxn_list[-1])
            if sp_name in FS_sp_list:
                parent_list.extend(self.remove_site_str(rxn_list[0]))

        return parent_list

    def find_origin_species(self, sp_name):
        "Find original species which is a gas species of the sp_name."
        parent_list = self.find_parent_species(sp_name)
        if len(parent_list) != 1:
            raise ValueError('%s has two parents: %s!' %
                             (sp_name, str(parent_list)))
        else:
            parent_species_str = parent_list[0]
            parent_species = self.split_species(parent_species_str)[-1]

        while parent_species not in self._owner.gas_names:
            sp_name = parent_species
            parent_list = self.find_parent_species(parent_species)
            if len(parent_list) != 1:
                raise ValueError('%s has two parents: %s!' %
                                 (sp_name, str(parent_list)))
            else:
                parent_species_str = parent_list[0]
                parent_species = self.split_species(parent_species_str)[-1]

        return parent_species  # origin species

    #original gas specie finding END

    #get related species and coefficients in all elementary rxns
    def get_related_adsorbates_wrt_product(self, product_name):
        """
        Expect a product name, return related adsorbate_names wrt the product.

        example:
        --------
        >>> m.parser.get_related_adsorbates('H2O_g')
        >>> {'H_s': 1, 'OH_s': 1}
        """
        #get corresponding adsorbate name
        product_ads = product_name.split('_')[0] + '_s'
        candidate_adsorbates = self.find_parent_species(product_ads)
        if len(candidate_adsorbates) <= 1:
            return {}
        else:  # firstly related adsorbates number must be larger than 1
            origin_sp_list = []
            related_adsorbates_dict = {}
            for sp_str in candidate_adsorbates:
                stoichiometry, sp_name = self.split_species(sp_str)
                related_adsorbates_dict.setdefault(sp_name, stoichiometry)
                #get origin species for sp_name
                origin_sp = self.find_origin_species(sp_name)
                origin_sp_list.append(origin_sp)
            origin_sp_set = set(origin_sp_list)
            if len(origin_sp_set) != 1:
                return {}
            else:
                return related_adsorbates_dict

    def get_related_adsorbates(self):
        """
        Get related adsorbate in all elementary rxns,
        related means there is a certain proportion relations
        among the coverages of these adsorbates.
        """
        if not hasattr(self._owner, 'total_rxn_list'):
            self.get_total_rxn_equation()
        products = self.strip_sp_list(self._owner.total_rxn_list[-1])
        related_adsorbates = []
        for product in products:
            single_related_ads_dict = \
                self.get_related_adsorbates_wrt_product(product)
            related_adsorbates.append(single_related_ads_dict)
        self._owner.related_adsorbates = related_adsorbates
        #get related adsorbates names
        related_adsorbate_names = []
        for rel_ads_dict in self._owner.related_adsorbates:
            if rel_ads_dict:
                keys_tup = tuple(sorted(rel_ads_dict.keys()))
                related_adsorbate_names.append(keys_tup)
        self._owner.related_adsorbate_names = related_adsorbate_names

        return related_adsorbates
