
import abc
from typing import List, TypeVar, Generic, Optional, Any


class Chromosome:
    def __init__(self, genes: Any):
        self.genes = genes


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


class Crossover(abc.ABC):
    """
    Abstract base class for a crossover operation.

    A crossover function defines how genetic material from two parent genotypes
    should be combined to produce a new genotype.

    Methods
    -------
    __call__(parent1: Chromosome, parent2: Chromosome) -> Chromosome
        Defines how the genotypes of the two parents are combined.
    """

    @abc.abstractmethod
    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """
        Combines two parent genotypes to create a new genotype.

        Parameters
        ----------
        parent1 : Chromosome
            The first parent Chromosome.
        parent2 : Chromosome
            The second parent Chromosome.

        Returns
        -------
        Chromosome
            A new chromosome resulting from combining the parent chromosomes.
        """
        pass


class Mutation(abc.ABC):
    """
    Abstract base class for a mutation operation.

    A mutation function defines how a genotype can be altered to introduce variation.

    Methods
    -------
    __call__(chromosome: Chromosome) -> Chromosome
        Defines how the genotype is mutated.
    """

    @abc.abstractmethod
    def __call__(self, chromosome: Chromosome) -> Chromosome:
        """
        Mutates the genotype to introduce variation.

        Parameters
        ----------
        chromosome : Chromosome
            The genotype to be mutated.

        Returns
        -------
        Chromosome
            The mutated genotype.
        """
        pass


T = TypeVar('T')


class Fitness(abc.ABC, Generic[T]):
    """
    Abstract base class for a fitness function.

    A fitness function evaluates the "fitness" or suitability of a genotype within the population.

    T must implement __lt__ to be sortable!

    Methods
    -------
    __call__(chromosome: Chromosome) -> T
        Evaluates the fitness of a given genotype.
    """

    @abc.abstractmethod
    def __call__(self, chromosome: Chromosome) -> T:
        """
        Evaluates the fitness of a given genotype.

        Parameters
        ----------
        chromosome : Chromosome
            The genotype to evaluate.

        Returns
        -------
        T
            The fitness score of the genotype.
            T must implement __lt__ to be sortable!
        """
        pass


class Individual(Generic[T]):
    """
    A class representing an individual in the population.

    An individual is characterized by its genotype and fitness score.


    Parameters
    ----------
    chromosome : Chromosome
        The genotype associated with this individual.

    Attributes
    ----------
    chromosome : Chromosome
        The genetic information of the individual.
    fitness : Optional[T]
        The fitness score of the individual, evaluated through a fitness function.

    Methods
    -------
    score_fitness(fitness_fn: Fitness[T])
        Evaluates and assigns a fitness score to the individual.
    """

    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome
        self.fitness: Optional[T] = None

    def score_fitness(self, fitness_fn: Fitness[T]):
        """
        Evaluates and assigns a fitness score to the individual.

        Parameters
        ----------
        fitness_fn : Fitness[T]
            The fitness function used to evaluate the individual.
        """
        self.fitness = fitness_fn(self.chromosome)


class Selection(abc.ABC):
    """
    Abstract base class for a selection operation.

    A selection function chooses a subset of individuals based on their fitness.

    Methods
    -------
    __call__(individuals: List[Individual], selection_rate: Optional[float]) -> List[Individual]
        Selects individuals from the population based on fitness.
    """

    @abc.abstractmethod
    def __call__(self, individuals: List[Individual]) -> List[Individual]:
        """
        Selects individuals from the population based on fitness.

        Parameters
        ----------
        individuals : List[Individual]
            The list of individuals to select from.
        selection_rate : Optional[float]
            The proportion of individuals to retain in the population.

        Returns
        -------
        List[Individual]
            The selected subset of individuals.
        """
        pass


class Population():
    """
    A class representing a population of individuals in a genetic algorithm.

    The population manages the creation, evolution, and evaluation of individuals.

    Parameters
    ----------
    n_individuals : int
        Number of individuals in the population.
    geno_type : GenoType
        The genotype structure for individuals in the population.
    fitness : Fitness
        Fitness function to evaluate each individual.
    crossover : Crossover
        Crossover function for combining parent genotypes.
    mutation : Mutation
        Mutation function to introduce variation in genotypes.
    selection : Selection
        Selection function for choosing individuals based on fitness.
    random_seed : int, optional
        Seed for random number generation, by default 42.

    Attributes
    ----------
    individuals : List[Individual]
        List of individuals in the population.

    Methods
    -------
    fitness()
        Calculates fitness scores for all individuals in the population.
    crossover(strategy: str = 'strongest_first')
        Applies crossover to the population based on a specified strategy.
    mutate()
        Applies mutation to all individuals in the population.
    select(selection_rate: float)
        Selects a subset of individuals based on their fitness.
    """

    def __init__(self, n_individuals: int, geno_type: GenoType, fitness: Fitness, crossover: Crossover, mutation: Mutation, selection: Selection, random_seed: int = 42):
        self.n_individuals: int = n_individuals
        self.geno_type: GenoType = geno_type
        self.individuals: List[Individual] = [Individual(self.geno_type.create_chromosome(None)) for _ in range(n_individuals)]
        self.crossover_fn: Crossover = crossover
        self.mutation_fn: Mutation = mutation
        self.selection_fn: Selection = selection
        self.fitness_fn: Fitness = fitness

    def __len__(self):
        return len(self.individuals)

    def fitness(self):
        """
        Calculates fitness scores for all individuals in the population.
        """

        for individual in self.individuals:
            individual.score_fitness(self.fitness_fn)

    def crossover(self, strategy: str = 'strongest_first'):
        """
        Applies crossover to the population based on a specified strategy.

        Parameters
        ----------
        strategy : str, optional
            Strategy for pairing individuals for crossover, by default 'strongest_first'.
        """

        # TODO: Implement a modular approach to how the crossover function should work.

        new_individuals: List[Individual] = []
        match strategy:
            case 'strongest_first':
                self.individuals = sorted(self.individuals, key=lambda individual: individual.fitness or 0, reverse=True)
                for i in range(0, len(self.individuals), 2):
                    if i + 1 < len(self.individuals):
                        parent1 = self.individuals[i]
                        parent2 = self.individuals[i + 1]
                        offspring1 = self.crossover_fn(parent1.chromosome, parent2.chromosome)
                        offspring2 = self.crossover_fn(parent2.chromosome, parent1.chromosome)
                        new_individuals.append(Individual(offspring1))
                        new_individuals.append(Individual(offspring2))
            case _:
                raise ValueError("Stategy needs to be one of: " + str('strongest_first'))

        self.individuals = new_individuals

    def mutate(self):
        """
        Applies mutation to all individuals in the population.
        """

        for individual in self.individuals:
            individual.chromosome = self.mutation_fn(individual.chromosome)

    def select(self):
        """
        Selects a subset of individuals based on their fitness.

        """

        self.individuals = self.selection_fn(self.individuals)
