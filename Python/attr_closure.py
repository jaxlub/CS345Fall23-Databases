# Jax Lubkowitz
# Oct 23, 23
# Closure algorithm for BCN Form

from typing import Tuple, List, Set


def attr_closure(F: List[Tuple[Set[str], Set[str]]],
                 X: Set[str]) -> Set[str]:
    """
    Compute the attribute closure of X given the FDs F
    :param F:
    :param X:
    :return:
    """

    result = X.copy()  # avoid modifying the original X

    while True:
        before = len(result)
        for (beta, gamma) in F:
            if beta.issubset(result):
                result = result.union(gamma)
        if len(result) == before:
            break
    return result


if __name__ == "__main__":
    """
    A -> B   A -> C  CG -> H  CG->I  B -> H  
    
    ({'A'},{'B'})
    """
    FDs = [
        ({'A'}, {'B'}),
        ({'A'}, {'C'}),
        ({'B'}, {'H'}),
        ({'G', 'C'}, {'H'}),
        ({'G', 'C'}, {'I'})
    ]
    print(attr_closure(FDs, {'A', 'G'}))
