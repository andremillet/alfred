
import timeit
from typing import Callable, Any, Dict

class BenchmarkingTool:
    """
    A tool for benchmarking the execution time of functions.
    """

    def run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> float:
        """
        Benchmarks the given function and returns the execution time.

        :param func: The function to benchmark.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: The execution time in seconds.
        """
        stmt = lambda: func(*args, **kwargs)
        return timeit.timeit(stmt, number=1000)

def get_tool() -> BenchmarkingTool:
    """Returns an instance of the BenchmarkingTool."""
    return BenchmarkingTool()
