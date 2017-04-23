import concurrent.futures


def execute_parallel(arg_tuples, num_threads=4):
    """A helper function to perform some operations in parallel on a threadpool.

    Arguments:
    arg_tuples -- a list of tuples that represent the arguments to be submitted
       into the executor; typically the first element of the tuple will a
       function, and the rest will be the arguments for the function
    num_threads (optional) -- the number of parallel threads to use

    Returns:
    a list with the results of executing arg_tuples

    Raises:
    any exception that is raised by the underlying execution
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(*args) for args in arg_tuples]
        return [f.result()
                for f in concurrent.futures.as_completed(futures)]
