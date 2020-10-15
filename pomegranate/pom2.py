from pomegranate import *

from pomegranate import DiscreteDistribution


seq = list('CGACTACTGACTACTCGCCGACGCGACTGCCGTCTATACTGCGCATACGGC')

d1 = DiscreteDistribution({'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25})
d2 = DiscreteDistribution({'A': 0.10, 'C': 0.40, 'G': 0.40, 'T': 0.10})

# Hidden Markov Model Setup
s1 = State( d1, name='background' )
s2 = State( d2, name='CG island' )

hmm = HiddenMarkovModel('Island Finder')
hmm.add_states(s1, s2)
hmm.add_transition( hmm.start, s1, 0.5 )
hmm.add_transition( hmm.start, s2, 0.5 )
hmm.add_transition( s1, s1, 0.5 )
hmm.add_transition( s1, s2, 0.5 )
hmm.add_transition( s2, s1, 0.5 )
hmm.add_transition( s2, s2, 0.5 )
hmm.bake()

#plt.figure( figsize=(10,6) )
hmm.plot()



hmm = HiddenMarkovModel()
hmm.add_states(s1, s2)
hmm.add_transition( hmm.start, s1, 0.5 )
hmm.add_transition( hmm.start, s2, 0.5 )
hmm.add_transition( s1, s1, 0.9 )
hmm.add_transition( s1, s2, 0.1 )
hmm.add_transition( s2, s1, 0.1 )
hmm.add_transition( s2, s2, 0.9 )
hmm.bake()

#plt.figure( figsize=(10,6) )
hmm.plot()
hmm_predictions = hmm.predict( seq )


import matplotlib.pyplot as plt

plt.show()

print("hmm pred: {}".format( ''.join( map( str, hmm_predictions ) ) ))

'''print "hmm state 0: {}".format( hmm.states[0].name )
print "hmm state 1: {}".format( hmm.states[1].name )
'''