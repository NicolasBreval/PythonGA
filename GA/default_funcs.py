from copy import deepcopy
import numpy as np
from typing import Iterable, Dict, NoReturn
from random import shuffle
from numpy.random import choice, uniform, randint

def default_selection_func(**kwargs: Dict) -> Iterable[np.ndarray]:
    population = kwargs['population']
    popsize = kwargs['popsize']
    fitnesses = kwargs['fitnesses']
    selection = sorted(population, key=lambda x: fitnesses[x.tostring()])[:int(popsize / 2)][:-2]
    return selection

def default_cross_func(**kwargs: Dict) -> Iterable[np.ndarray]:
    children = []

    selection = kwargs['selection']
    cross_prop = kwargs['default_cross_prop']

    shuffle(selection)

    for i in range(0, len(selection), 2):
        first_parent = selection[i]
        second_parent = selection[(i + 1) % len(selection)]

        A = first_parent[:int(cross_prop * first_parent.shape[0])]
        B = first_parent[int(cross_prop * first_parent.shape[0]):]
        C = second_parent[:int(cross_prop * first_parent.shape[0])]
        D = second_parent[int(cross_prop * first_parent.shape[0]):]

        children.append(np.concatenate((A, D), axis = 0))
        children.append(np.concatenate((C, B), axis = 0))

    return children
            

def default_mutation_func(**kwargs: Dict) -> NoReturn:
    cross_children = kwargs['cross_children']
    chromosome_limits = kwargs['chromosome_limits']
    mutation_prob = kwargs['default_mutation_prob']
    iterations = kwargs['iterations']
    max_iters = kwargs['max_iters']
    is_float = kwargs['is_float']

    mutated = deepcopy(cross_children)

    for i in range(len(mutated)):
        child = mutated[i]

        for j in range(child.shape[0]):
            mut_prob = mutation_prob * (iterations / max_iters) 
            modify = bool(choice([True, False], 1, p=[mut_prob, 1 - mut_prob]))

            if modify:
                if is_float:
                    new_val = child[j] * uniform(low=chromosome_limits[j], high=chromosome_limits[j] + 1, size=1)
                else:
                    new_val = child[j] * randint(low=chromosome_limits[j], high=chromosome_limits[j] + 1, size=1)
                
                child[j] = new_val
    
    return mutated
