import numpy as np
from typing import Callable, NoReturn, Union
from numpy import random
from GA.exceptions import *
from datetime import datetime
from GA.default_funcs import *
from copy import deepcopy
from GA.historical import Historical

class GeneticAlgorithm:

    def __init__(
        self,
        chromosome_limits: np.ndarray,
        chromosome_type: np.dtype,
        fitness_func: Callable[[np.ndarray], np.ndarray],
        selection_func: Callable[[np.ndarray], np.ndarray] = None, 
        cross_func: Callable[[np.ndarray], np.ndarray] = None, 
        mutation_func: Callable[[np.ndarray], np.ndarray] = None,
        stop_fitness: Union[np.ndarray, float] = None,
        default_cross_prop: float = 0.5,
        default_mutation_prob: float = 0.5,
        popsize: int = 10,
        max_iters: int = 10,
        verbose = False
    ) -> NoReturn:
        
        ############################
        ## CHECK INPUT DATA TYPES ##
        ############################
        if type(chromosome_limits) is not np.ndarray or (type(chromosome_limits) is np.ndarray and chromosome_limits.shape[1] != 2):
            raise WrongInputTypeError("chromosome_limits input argument must be numpy array with shape (N, 2)")

        try:
            if np.dtype(chromosome_type).char != '?' and np.dtype(chromosome_type).char not in (np.typecodes['Float'] + np.typecodes['AllInteger']):
                raise WrongInputTypeError("chromosome_type argument must be a valid numpy boolean, float o integer")
        except TypeError:
            raise WrongInputTypeError("chromosome_type argument must be a valid numpy dtype")

        if np.dtype(chromosome_type).char == '?':
            for limit in range(len(chromosome_limits)):
                if limit[0] > 1 or limit[0] < 0 or limit[1] > 1 or limit[0] < 0:
                    raise WrongInputTypeError("if chromosomes are boolean, limits must be 0 or 1")

        if not callable(fitness_func):
            raise WrongInputTypeError("fitness_func input argument must be a callable function and must be return a np.ndarray value as result")

        if selection_func is not None and not callable(selection_func):
            raise WrongInputTypeError("selection_func input argument must be a callable function and must be return a np.ndarray value as result")

        if cross_func is not None and not callable(cross_func):
            raise WrongInputTypeError("cross_func input argument must be a callable function and must be return a np.ndarray value as result")

        if mutation_func is not None and not callable(mutation_func):
            raise WrongInputTypeError("mutation_func input argument must be a callable function and must be return a np.ndarray value as result")

        if stop_fitness is not None and type(stop_fitness) not in [np.ndarray, float, int]:
            raise WrongInputTypeError("stop_fitness input argument must be a np.ndarray or float object")

        if type(default_cross_prop) not in [float, int]:
            raise WrongInputTypeError("default_cross_prop input argument must be a float value")

        if default_cross_prop > 1 or default_cross_prop < 0:
            raise WrongInputTypeError("default_cross_prop input argument value must be between 1 and 0, both included")

        if type(default_mutation_prob) not in [float, int]:
            raise WrongInputTypeError("default_mutation_prob input argument must be a float value")

        if default_mutation_prob > 1 or default_mutation_prob < 0:
            raise WrongInputTypeError("default_mutation_prob input argument value must be between 1 and 0, both included")
        
        if type(popsize) is not int:
            raise WrongInputTypeError("popsize input argument must be a integer object")

        if popsize % 2 != 0:
            raise WrongInputTypeError("popsize input argument must be a pair value")

        if type(max_iters) is not int:
            raise WrongInputTypeError("max_iters input argument must be a integer object")

        #####################################
        ## ADD VALUES TO OBJECT PROPERTIES ##
        #####################################
        self.chromosome_limits = chromosome_limits
        self.chromosome_type = chromosome_type
        self.fitness_func = fitness_func
        self.selection_func = selection_func if selection_func is not None else default_selection_func
        self.cross_func = cross_func if cross_func is not None else default_cross_func
        self.mutation_func = mutation_func if mutation_func is not None else default_mutation_func
        self.stop_fitness = stop_fitness
        self.default_cross_prop = default_cross_prop
        self.default_mutation_prob = default_mutation_prob
        self.popsize = popsize
        self.max_iters = max_iters
        self.verbose = verbose
        self.population = [] # Current population
        self.fitnesses =  {}
        self.best = None # Best individual: an array with two positions (individual's representation, individual's fitness)
        self.is_float = np.dtype(self.chromosome_type).char in np.typecodes['Float']
        self.is_integer = np.dtype(self.chromosome_type).char in np.typecodes['AllInteger']
        self.is_boolean = np.dtype(self.chromosome_type).char == '?'
        self.iterations = 0

    def run(self) -> NoReturn:
        self.population = []
        self.fitnesses =  {}
        self.iterations = 0
        self.historical = Historical()

        # First random population
        self.log("Generating random population")
        self.generate_random_pop()

        self.log("Evaluating initial population")
        self.get_population_fitness()

        # Iterations
        self.log("Running iterations")
        for i in range(self.max_iters):
            self.log(f"Iteration {i + 1} of {self.max_iters}")

            # Select from population
            self.log("\tSelecting population")
            self.selection = self.selection_func(**self.__dict__)

            # Cross selected population and generate individuals
            self.log("\tCrossing chromosomes")
            self.cross_children = self.cross_func(**self.__dict__)

            # Mutate new individuals
            self.log("\tMutating new individuals")
            self.mutated = self.mutation_func(**self.__dict__)

            # Conform new population
            self.log("\tConforming new population")
            self.population = self.selection + self.mutated

            # Evaluate new population
            self.log("\tEvaluating new population")
            self.get_population_fitness()

            # Select current best individual
            self.log("Selecting best individual")
            self.select_best()
            self.log(f"Current best individual: {self.best}")

            # Save historical
            self.historical.add_to_historical(self.population, self.fitnesses, self.best)

            if self.best[1] == self.stop_fitness:
                self.log("Stopping fitness value has been reached")
                break
            
            self.iterations = i + 1

    def generate_random_pop(self) -> NoReturn:
        random_pop = []

        for _ in range(self.popsize):
            individual = np.array([], dtype = self.chromosome_type)

            for i in range(len(self.chromosome_limits)):
                low = self.chromosome_limits[i][0]
                high = self.chromosome_limits[0][1] + 1

                if not self.is_float:
                    individual = np.concatenate((individual, np.random.randint(low=low, high=high, size=1)), axis=0)
                else:
                    individual = np.concatenate((individual, np.random.uniform(low=low, high=high, size=1)), axis=0)

            random_pop.append(individual)
        
        self.population.extend(random_pop)

    def get_population_fitness(self) -> NoReturn:
        for individual in self.population:
            _id = individual.tostring()

            if _id not in self.fitnesses:
                self.fitnesses[_id] = self.fitness_func(individual)

    def select_best(self) -> NoReturn:
        individuals_with_fitness = [(individual, self.fitnesses[individual.tostring()]) for individual in self.population]
        individuals_with_fitness.sort(key = lambda x: x[1])
        self.best = individuals_with_fitness[0]

    def log(self, message: str) -> NoReturn:
        if self.verbose:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")