from .general import Chromosome, Crossover
import numpy as np


class SinglePointCrossover(Crossover):
    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        crossover_point = np.random.randint(1, len(parent1.genes))
        offspring = np.concatenate((parent1.genes[:crossover_point], parent2.genes[crossover_point:]))
        return Chromosome(offspring)
