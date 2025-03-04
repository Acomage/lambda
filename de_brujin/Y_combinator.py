from uint import IsZero, Predecessor, Mul, int_to_lambda, lambda_to_int
from bool import IF
from parser import parser
import cProfile
import pstats

Y_combinator = parser("λf.(λx.f (x x)) (λx.f (x x))")
One = parser("λf.λx.(f x)")
Two = parser("λf.λx.(f (f x))")
Three = parser("λf.λx.(f (f (f x)))")
If_false_text = f"((({Mul}) x) (f (({Predecessor}) x)))"
Factorial_generator_text = (
    f"λf.λx.(((({IF}) (({IsZero}) x)) ({One})) ({If_false_text}))"
)
Factorial_generator = parser(Factorial_generator_text)


def test():
    print(lambda_to_int(Y_combinator(Factorial_generator)(int_to_lambda(4))))


if __name__ == "__main__":
    #     cProfile.run("test()", "profile_output")
    #     with open("profile_stats.txt", "w") as f:
    #         p = pstats.Stats("profile_output", stream=f)
    #         p.sort_stats("cumulative").print_stats()
    test()
