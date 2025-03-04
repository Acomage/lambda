from lambda_term import LambdaTerm
from parser import parser


def n_tuple_constructor(n: int) -> LambdaTerm:
    left = ""
    mid = "λf."
    right = "f"
    for i in range(n):
        left += f"λi{i}."
        mid += "("
        right += f" i{i})"
    return parser(left + mid + right)


def mth_in_n_list(m: int, n: int) -> LambdaTerm:
    left = ""
    right = f"i{m}"
    for i in range(n):
        left += f"λi{i}."
    return parser(left + right)


def list_to_lambda_term(lst: list) -> LambdaTerm:
    n = len(lst)
    constructor = n_tuple_constructor(n)
    lambda_term = constructor
    for i in range(n):
        lambda_term = lambda_term(lst[i])
    return lambda_term.super_beta_reduce()


Pair = n_tuple_constructor(2)
First = mth_in_n_list(0, 2)
Second = mth_in_n_list(1, 2)

if __name__ == "__main__":
    zero = parser("λf.λx.x")
    one = parser("λf.λx.(f x)")
    two = parser("λf.λx.(f (f x))")
    triple = list_to_lambda_term([zero, one, two])
    first = mth_in_n_list(0, 3)
    second = mth_in_n_list(1, 3)
    third = mth_in_n_list(2, 3)
    print(triple(first))
    print(triple(second))
    print(triple(third))
