from utils import execute_parallel


class Accumulator:
    accumulator = 0

    @staticmethod
    def accumulate(value):
        Accumulator.accumulator += value
        return Accumulator.accumulator


def test_parallel():
    results = execute_parallel(
        [(Accumulator.accumulate, 1), (Accumulator.accumulate, 3)])
    assert len(results) == 2
    assert Accumulator.accumulator == 4  # 1 and 3 were accumulated
