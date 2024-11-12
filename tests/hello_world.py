import genetic


def diff_letters(a, b):
    return sum(a[i] != b[i] for i in range(len(a)))


class StringGenPopulation(genetic.Population):
    def __init__(self, target, geno_type, n_individuals):
        super().__init__(geno_type, n_individuals)
        self.target = target

    def fitness(self, geno_type):
        # Because geno_type is the same as pheno_type in this case we can just
        # create our own fitness function for the geno_type
        return -diff_letters(geno_type, self.target)


def test_hello_world():
    target_phrase = "Hello world!"
    target_len = len(target_phrase)
    geno_type = genetic.String(target_len)

    population = StringGenPopulation(target=target_phrase, geno_type=geno_type, n_individuals=100)
    crossover = genetic.StringSinglePointCrossover(target_len)
    mutation = genetic.StringMutation(0.01)

    for generation in range(100):
        print("generation " + str(generation))
        population.simulate().select().crossover(crossover).mutate(mutation)
