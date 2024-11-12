from .general import GenoType, Chromosome
import numpy as np


class BitVectorGenoType(GenoType):
    """
    A genotype representation as a vector of bits.

    This class initializes a genotype as a vector of binary values (0 or 1) of a specified length.

    Parameters
    ----------
    length : int
        The length of the bit vector.

    Attributes
    ----------
    bit_vector : np.ndarray
        The binary vector representing the genotype.

    Methods
    -------
    initialize(random_seed: int = 42) -> BitVectorGenoType
        Initializes the bit vector with random binary values.
    """

    def __init__(self, length: int):
        self.length = length

    def create_chromosome(self) -> Chromosome:
        return Chromosome(np.random.randint(0, 2, size=self.length))
