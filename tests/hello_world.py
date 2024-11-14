from genetic import BitGenoType, Chromosome, BitFlipMutation, SinglePointCrossover, Individual, RouletteWheelSelection
import numpy as np
from typing import List


def test_BitGenoType_invariant():
    geno_type: BitGenoType = BitGenoType(5)
    chromosome: Chromosome = geno_type.create_chromosome()
    assert np.all((chromosome.genes == 1) | (chromosome.genes == 0))


def test_BitGenoType_BitFlipMutation_invariant():
    geno_type: BitGenoType = BitGenoType(5)
    chromosome: Chromosome = geno_type.create_chromosome()

    mutation: BitFlipMutation = BitFlipMutation(mutation_rate=0.5)

    new_chromosome: Chromosome = mutation.mutate(chromosome)

    assert chromosome != new_chromosome

    assert np.all((new_chromosome.genes == 1) | (new_chromosome.genes == 0))


def test_BitGenoType_SinglePointCrossover():
    geno_type: BitGenoType = BitGenoType(5)
    chromosome: Chromosome = geno_type.create_chromosome()
    chromsome2: Chromosome = geno_type.create_chromosome()

    crossover: SinglePointCrossover = SinglePointCrossover()

    child: Chromosome = crossover.crossover(chromosome, chromsome2)

    # Don't really have a good test here
    assert child != chromosome and child != chromsome2


def test_BitGenoType_RouletteWheelSelection():
    geno_type: BitGenoType = BitGenoType(5)
    chromosome: Chromosome = geno_type.create_chromosome()
    chromsome2: Chromosome = geno_type.create_chromosome()
    individuals: List[Individual] = [Individual(chromosome), Individual(chromsome2)]

    # Manually setting a fitness
    individuals[0].fitness = 10
    individuals[1].fitness = -10

    selection: RouletteWheelSelection = RouletteWheelSelection(0.5)  # Half of the population needs to die out
    new_individuals: List[Individual] = selection.select(individuals)

    assert len(new_individuals) == 1
    assert new_individuals[0].fitness == 10

    individuals[1].fitness = 0
    new_individuals: List[Individual] = selection.select(individuals)
