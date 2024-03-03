class NumberCoincidence:
    MIN_CONFIDENCE = 0.9

    def __init__(self, number: int, matching_coincidence: float, x_coordinate: float):
        self.number = number
        self.matching_coincidence = matching_coincidence
        self.x_coordinate = x_coordinate

    def __str__(self):
        return f'NumberCoincidence(number={self.number}, matching_coincidence={self.matching_coincidence}, x_coordinate={self.x_coordinate})'
