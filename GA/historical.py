from typing import Iterable, Dict, NoReturn
import pickle
from GA.exceptions import *
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class Historical:

    def __init__(self) -> NoReturn:
        self.population = []
        self.fitnesses = {}
        self.best = []

    def add_to_historical(self, population: Iterable, fitnesses: Dict, best: tuple) -> NoReturn:
        self.population.append(population)
        self.fitnesses.update(fitnesses)
        self.best.append(best)

    def export_historical(self, filename: str) -> NoReturn:
        with open(filename, 'wb') as pfile:
            pickle.dump(self.__dict__, pfile)
    
    def import_historical(self, filename: str) -> NoReturn:
        with open(filename, 'rb') as pfile:
            obj = pickle.load(pfile)

            if not isinstance(obj, dict):
                raise HistoricalImportFormatError("The object you are trying to import is not a Historical object")
            elif 'population' in obj and 'fitnesses' in obj and 'best' in obj:
                self.population = deepcopy(obj['population'])
                self.fitnesses = deepcopy(obj['fitnesses'])
                self.best = deepcopy(obj['best'])

    def show_best_historical(self) -> NoReturn:
        fig, ax = plt.subplots()
        fig.suptitle("Best fitness evolution", fontsize=20)
        plt.xlabel('Iteration')
        plt.ylabel('Best fitness')

        x = [i + 1 for i in range(len(self.best))]
        y = [x[1] for x in self.best]
        ax.plot(x, y)


        plt.show()


    def __next__(self, event):
        if self.current_index < len(self.population) - 1:
            self.current_index += 1
            self.__update__()
            self.__set__()
            

    def __prev__(self, event):
        if self.current_index > 0:
            self.current_index -= 1
            self.__update__()
            self.__set__()

    def __update__(self):
        self.x = [i for i in range(len(self.population[self.current_index]))]
        self.y = [self.fitnesses[x.tostring()] for x in self.population[self.current_index]]
    
    def __set__(self):
        self.ax.clear()
        self.ax.scatter(self.x, self.y)

        for i in self.x:
            self.ax.annotate(f"{self.y[i]}", (self.x[i], self.y[i]))

        self.fig.suptitle(f"Iteration {self.current_index + 1}", fontsize=20)
        plt.axes(self.ax)
        plt.xlabel('Individual')
        plt.ylabel('Fitness')
        plt.draw()

    def show_population_historical(self) -> NoReturn:
        self.current_index = 0

        self.fig, self.ax = plt.subplots()
        self.__update__()
        self.__set__()

        axprev = plt.axes([0.7, 0.00, 0.1, 0.06])
        axnext = plt.axes([0.81, 0.00, 0.1, 0.06])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.__next__)
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(self.__prev__)


        plt.show()

    def export_to_text_file(self, filename):
        with open(filename, 'w') as file:

            for i in range(len(self.population)):
                file.write(f"#### Iteration {i + 1} #############################\n\n")

                for index, pop in enumerate(self.population[i]):
                    file.write(f"\tIndividual {index + 1}: {list(pop)} -> {self.fitnesses[pop.tostring()]}\n")
                
                file.write(f"\n\tBest: {list(self.best[i][0])} -> {self.best[i][1]}\n\n")
                file.write("################################################\n\n")

