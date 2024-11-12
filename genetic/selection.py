from .general import Individual, Selection
from typing import List
import numpy as np


class RouletteWheelSelection(Selection):
    """
    Each individual has a probability of being selected that is proportional to its fitness.
    This is similar to spinning a roulette wheel, where individuals with higher fitness occupy
    larger portions of the wheel.
    """

    def __init__(self, selection_rate: float):
        assert selection_rate < 1.0, "Selection rate needs to be less than 1.0"
        assert selection_rate > 0.0, "Selection rate needs to be larger than 0.0"
        self.selection_rate = selection_rate

    def __call__(self, individuals: List[Individual]) -> List[Individual]:
        fitnesses = np.array([individual.fitness for individual in individuals])
        probabilities = fitnesses / np.sum(fitnesses)
        selected_indices = np.random.choice(len(individuals), size=np.floor(self.selection_rate * len(individuals)).astype(int), p=probabilities)
        return [individuals[i] for i in selected_indices]
