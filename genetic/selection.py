from .general import Individual, Selection
from typing import List
import numpy as np


class RouletteWheelSelection(Selection):
    def __init__(self, selection_rate: float):
        assert selection_rate < 1.0, "Selection rate needs to be less than 1.0"
        assert selection_rate > 0.0, "Selection rate needs to be larger than 0.0"
        self.selection_rate = selection_rate

    def select(self, individuals: List[Individual]) -> List[Individual]:
        fitnesses = np.array([individual.fitness for individual in individuals])
        probabilities = fitnesses / np.sum(fitnesses)
        selected_indices = np.random.choice(len(individuals), size=np.floor(self.selection_rate * len(individuals)).astype(int), p=probabilities)
        return [individuals[i] for i in selected_indices]
