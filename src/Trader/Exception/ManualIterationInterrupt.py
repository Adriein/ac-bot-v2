class ManualIterationInterrupt(Exception):
    def __init__(self):
        super().__init__(f'ManualIterationInterrupt')