import numpy as np
from .general import Chromosome, Mutation


class BitFlipMutation(Mutation):

    def __init__(self, mutation_rate: float):
        """
        Parameters
        ----------
        mutation_rate : float, optional
            Probability of each bit flipping, by default 0.01.
        """
        self.mutation_rate = mutation_rate

    def __call__(self, chromosome: Chromosome) -> Chromosome:
        """
        Perform bit flip mutation on a bit vector with a given mutation rate.

        Parameters
        ----------
        chromosome: chromosome
            Needs to be chromosome made from a BitVectorGenoType

        Returns
        -------
        chromosome
            Mutated chromosome.
        """
        mutation_mask = np.random.rand(len(chromosome.genes)) < self.mutation_rate
        mutated_vector = np.copy(chromosome.genes)
        mutated_vector[mutation_mask] = 1 - mutated_vector[mutation_mask]
        return Chromosome(mutated_vector)
