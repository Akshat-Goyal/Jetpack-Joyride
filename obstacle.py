import numpy as np

class Obstacle:
    def __init__(self, disp):
        self._disp = disp
        self._dim = self._disp.shape

    