import sys

sys.path.append('D:\Dropbox\Code\Python\kinetic\Pynetics')
from pynetics import model

#create micro kinetic model instance
m = model.KineticModel(setup_file='furfural.mkm')

m.parser.parse_data()  # parse data from rel_energy.py
m.solver.get_data_dict()  # solver get data from parser
m.solver.get_rate_constants()
m.solver.get_rate_expressions(m.solver.rxns_list)

for i, rxn_equation in enumerate(m.rxn_expressions):
    print 'Plotting diagram '+str(i)+'...'
    m.plotter.plot_single_energy_diagram(rxn_equation, show_mode='save')
    print 'Ok.'

print "Plotting multi_energy_diagram..."
m.plotter.plot_multi_energy_diagram(m.rxn_expressions, show_mode='save')
print 'Ok.\n'

if 'c' in sys.argv[1]:
    print 'Correct free energies...'
    m.solver.correct_energies()
    print 'Ok.'

b_cvg = m.solver.boltzmann_coverages()
#init_cvg = (b_cvg[0]*(1e-2), b_cvg[1], b_cvg[-1]*(1e-2))
cvg = m.solver.get_steady_state_cvgs(b_cvg)
print m.adsorbate_names