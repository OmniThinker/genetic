
import abc
from typing import List, TypeVar, Generic, Optional, Any
import math


class Chromosome:
    def __init__(self, genes: Any):
        self.genes = genes

    def __repr__(self) -> str:
        return f'Chromsome({self.genes})'

    def __eq__(self, o):
        self.genes != o.genes


class GenoType(abc.ABC):
    """
    Abstract base class for a genotype representation.

    A genotype defines the genetic information of an individual and
    may contain various representations, such as floating-point vectors, strings, etc.
    Users can implement their own genotypes by inheriting from this class.

    Methods
    -------
    initialize()
        Initializes the genotype with starting values.
    """
    @abc.abstractmethod
    def create_chromosome(self) -> Chromosome:
        """
        Initializes a genotype.

        """
        pass


T = TypeVar('T')


class Fitness(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def __call__(self, chromosome: Chromosome) -> T:
        pass


class Individual(Generic[T]):
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome
        self.fitness: Optional[T] = None

    def score_fitness(self, fitness_fn: Fitness[T]):
        self.fitness = fitness_fn(self.chromosome)

    def __lt__(self, other):
        f1 = self.fitness or 0
        f2 = other.fitness or 0
        return f1 < f2

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}(genes={self.chromosome.genes}, fitness={self.fitness})'


class Population():
    def __init__(self, n_individuals: int, geno_type: GenoType, fitness: Fitness):
        self.n_individuals: int = n_individuals
        self.geno_type: GenoType = geno_type
        self.individuals: List[Individual] = [Individual(self.geno_type.create_chromosome()) for _ in range(n_individuals)]
        self.fitness_fn: Fitness = fitness

    def __len__(self):
        return len(self.individuals)

    def best_individual(self):
        return max(self.individuals)

    def fitness(self):
        # TODO: Parallellize the shit out of me, taking max workers etc.
        for individual in self.individuals:
            individual.score_fitness(self.fitness_fn)
        return self

    def __or__(self, func):
        # Overloading or operator
        return func(self)


class Selection(abc.ABC):
    @abc.abstractmethod
    def select(self, individuals: List[Individual]) -> List[Individual]:
        pass

    def __call__(self, population: Population) -> Population:
        population.individuals = self.select(population.individuals)
        return population


class Mutation(abc.ABC):
    @abc.abstractmethod
    def mutate(self, chromosome: Chromosome) -> Chromosome:
        pass

    def __call__(self, population: Population) -> Population:
        for individual in population.individuals:
            individual.chromosome = self.mutate(individual.chromosome)
        return population


class Crossover(abc.ABC):

    @abc.abstractmethod
    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        pass

    def __call__(self, population: Population) -> Population:
        new_individuals: List[Individual] = []
        population.individuals = sorted(population.individuals, key=lambda individual: individual.fitness or 0, reverse=True)
        # Keep the strongest 50 % of individuals
        keep_count: int = int(math.floor(population.n_individuals * 0.5))

        for individual in population.individuals[:keep_count]:
            new_individuals.append(individual)

        for i in range(0, keep_count, 2):
            if i + 1 < len(population.individuals):
                parent1 = population.individuals[i]
                parent2 = population.individuals[i + 1]
                offspring1 = self.crossover(parent1.chromosome, parent2.chromosome)
                offspring2 = self.crossover(parent2.chromosome, parent1.chromosome)
                new_individuals.append(Individual(offspring1))
                new_individuals.append(Individual(offspring2))

        population.individuals = new_individuals
        return population
