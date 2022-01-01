import numpy as np

class Utils():

    def tuplearray(tlist=None):
        if isinstance(tlist, np.ndarray):
            # Test the first element, if a tuple, do nothing
            if len(tlist) > 0 and isinstance(tlist[0], tuple): return tlist

            # Convert elements to tuples and return a new array
            a = np.empty(len(tlist), dtype=object)
            for i in range(len(tlist)):
                a[i] = tuple(tlist[i])
            return a
        else:
            # Need to create an ndarray
            if tlist == None:
                # Empty list
                tlist = []
            elif isinstance(tlist, tuple):
                # One tuple
                tlist = [tlist]
            elif isinstance(tlist, list):
                # Empty list
                if len(tlist) == 0:
                    pass
                elif isinstance(tlist[0], list):
                    # Assume list of lists of values
                    tlist = [tuple(x) for x in tlist]
                elif isinstance(tlist[0], tuple):
                    # A list of tuples
                    pass
                else:
                    # Assume a single list of values
                    tlist = [tuple(tlist)]

            a = np.empty(len(tlist), dtype=object)
            a[:] = tlist
            return a
