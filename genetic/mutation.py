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


class GaussianMutation(Mutation):
    def __init__(self, mutation_rate=0.1, mutation_strength=0.2):
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def mutate(self, chromosome: Chromosome) -> Chromosome:
        mutated_vector = chromosome.genes.copy()

        for i in range(len(mutated_vector)):
            if np.random.rand() < self.mutation_rate:
                # Apply mutation by adding a small random value to the gene
                mutation = np.random.uniform(-self.mutation_strength, self.mutation_strength)
                mutated_vector[i] += mutation

        return Chromosome(mutated_vector)
