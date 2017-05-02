from utils import execute_parallel
import os

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

def _abs_file(filename):
    """Given a filename relative to the current file, returns the absolute filename"""
    absolute_current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(absolute_current_dir, filename)