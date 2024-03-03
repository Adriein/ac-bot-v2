class NumberCoincidence:
    def __init__(self, number: int, matching_coincidence: float, x_coordinate: float):
        self.number = number
        self.matching_coincidence = matching_coincidence
        self.x_coordinate = x_coordinate

    def __eq__(self, other):
        if isinstance(other, NumberCoincidence):
            return self.matching_coincidence == other.matching_coincidence and self.x_coordinate == other.x_coordinate

        return False

    def __gt__(self, other):
        if isinstance(other, NumberCoincidence):
            return self.x_coordinate > other.x_coordinate

        return False

    def __str__(self):
        return f'Tile(number={self.number}, matching_coincidence={self.matching_coincidence}, x_coordinate={self.x_coordinate})'
