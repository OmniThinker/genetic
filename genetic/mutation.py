import numpy as np
from .general import Chromosome, Mutation


class BitFlipMutation(Mutation):

    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def mutate(self, chromosome: Chromosome) -> Chromosome:
        mutation_mask = np.random.rand(len(chromosome.genes)) < self.mutation_rate
        mutated_vector = np.copy(chromosome.genes)
        mutated_vector[mutation_mask] = 1 - mutated_vector[mutation_mask]
        return Chromosome(mutated_vector)
