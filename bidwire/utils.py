import concurrent.futures

def execute_parallel(fn, *iterables, num_threads=4):
    """A helper function to perform a function on different arguments in parallel.

    This is a thin wrapper on top of concurrent.futures.Executor.map. See:
    https://docs.python.org/3/library/concurrent.futures.html

    Arguments:
    fn -- the function to execute
    iterables -- the iterable with arguments to pass to func in different invocations;
        if more than one iterable is provided, then func must take that number of arguments
    num_threads (optional) -- the number of parallel threads to use

    Returns:
    a generator with the results of executing arg_tuples

    Raises:
    any exception that is raised by the underlying execution
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        return executor.map(fn, *iterables)
