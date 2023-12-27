from Magritte.descriptions.MADescription_class import MADescription
from Magritte.visitors.MAEqualityTester_visitor import MAEqualityTester, MAInequalityFound


class MAEqualityTesterFuzzy(MAEqualityTester):

    def __init__(self, tolerance: int = 0):
        super().__init__()
        self._tolerance = tolerance  # tolerance in seconds

    def visitDateAndTimeDescription(self, description: MADescription):
        value1 = description.accessor.read(self._model1)
        value2 = description.accessor.read(self._model2)
        if value1 is None:
            return value2 is None
        diff = (value1 - value2).total_seconds()
        if abs(diff) > self._tolerance:
            raise MAInequalityFound()
