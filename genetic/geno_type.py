from .general import GenoType, Chromosome
import numpy as np
from typing import Optional


class BitGenoType(GenoType):
    def __init__(self, size: int):
        self.size = size

    def create_chromosome(self) -> Chromosome:
        return Chromosome(np.random.randint(0, 2, size=self.size))


class FloatGenoType(GenoType):
    def __init__(self, size: int, low: float = 0.0, high: float = 1.0, mean: float = 0.0, std: float = 1.0, distribution: str = 'uniform'):
        self.size: int = size
        self.low: float = low
        self.high: float = high
        self.mean: float = mean
        self.std: float = std
        self.distribution: str = distribution

    def create_chromosome(self) -> Chromosome:
        match self.distribution:
            case 'uniform':
                genes = (self.high - self.low) * np.random.random_sample(size=self.size) + self.low
            case 'normal':
                genes = np.random.normal(self.mean, self.std, size=self.size)
            case _:
                raise ValueError("Distribution is not recognized must be one of: " + "'uniform', or 'normal'")

        return Chromosome(genes)


class IntegerGenoType(GenoType):
    def __init__(self, size: int, low: int = 0, high: Optional[int] = None):
        self.size: int = size
        self.low: int = low
        self.high: Optional[int] = high

    def create_chromosome(self) -> Chromosome:
        return Chromosome(np.random.randint(self.low, self.high, size=self.size))


class PermutationGenoType(GenoType):
    def __init__(self, low: int = 0, high: int = 10, rng: Optional[list[int]] = None):
        self.low: int = low
        self.high: int = high
        self.rng = rng

    def create_chromosome(self) -> Chromosome:
        if self.rng:
            return Chromosome(np.random.permutation(self.rng))
        else:
            return Chromosome(np.random.permutation(range(self.low, self.high)))
