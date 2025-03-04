from lambda_term import LambdaTerm
from tuple import Pair, First, Second
from bool import TRUE, FALSE, AND
from parser import parser

Zero = parser("λf.λx.x")
Successor = parser("λn.λf.λx.(f ((n f) x))")
Add = parser("λm.λn.λf.λx.((m f) ((n f) x))")
Mul = parser("λm.λn.λf.λx.((m (n f)) x)")
slide_first = f"(p {Second})"
slide_second = f"({Successor}) ({slide_first})"
after_slide = f"({Pair}) ({slide_first}) ({slide_second})"
Slide = parser(f"λp.{after_slide}")
Origin = Pair(Zero)(Zero)
Predecessor_text = f"λn.(n ({Slide})) ({Origin}) ({First})"
Predecessor = parser(Predecessor_text)
Minus_text = f"λm.λn.n ({Predecessor}) m"
Minus = parser(Minus_text)
IsZero_text = f"λn.((n λp.{FALSE}) {TRUE})"
IsZero = parser(IsZero_text)
LessOrEqual_text = f"λa.λb.({IsZero_text}) (({Minus_text}) a b)"
LessOrEqual = parser(LessOrEqual_text)
Equal_text = f"λa.λb.({AND}) (({LessOrEqual_text}) a b) (({LessOrEqual_text}) b a)"
Equal = parser(Equal_text)


def int_to_lambda(n: int) -> LambdaTerm:
    if n == 0:
        return Zero
    else:
        return Successor(int_to_lambda(n - 1))


def lambda_to_int(num: LambdaTerm) -> int:
    return num.__str__().count("(")


if __name__ == "__main__":
    for i in range(10):
        print(i, "=", lambda_to_int(int_to_lambda(i)))
    for i in range(10):
        for j in range(10):
            print(
                i, "+", j, "=", lambda_to_int(Add(int_to_lambda(i))(int_to_lambda(j)))
            )
    for i in range(10):
        for j in range(10):
            print(
                i, "*", j, "=", lambda_to_int(Mul(int_to_lambda(i))(int_to_lambda(j)))
            )
    test_list = Pair(Zero)(Zero).super_beta_reduce()
    print(Slide(test_list)(First))
    print(Slide(test_list)(Second))
    for i in range(1, 10):
        for j in range(1, i):
            print(
                i, "-", j, "=", lambda_to_int(Minus(int_to_lambda(i))(int_to_lambda(j)))
            )
    for i in range(10):
        print(i, IsZero(int_to_lambda(i)))
    for i in range(5):
        for j in range(5):
            print(i, "=", j, "=", Equal(int_to_lambda(i))(int_to_lambda(j)))
