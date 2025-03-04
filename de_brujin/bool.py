from lambda_term import LambdaTerm
from parser import parser


def bool_to_lambda(value: bool) -> LambdaTerm:
    if value:
        return parser("λx.λy.x")
    else:
        return parser("λx.λy.y")


def lambda_to_bool(term: LambdaTerm) -> bool:
    if term == parser("λx.λy.x"):
        return True
    elif term == parser("λx.λy.y"):
        return False
    else:
        raise ValueError(f"Cannot convert {term} to bool")


AND = parser("λp.λq.((p q) p)")
OR = parser("λp.λq.((p p) q)")
NOT = parser("λp.((p λx.λy.y) λx.λy.x)")
IF = parser("λp.λa.λb.((p a) b)")
TRUE = parser("λx.λy.x")
FALSE = parser("λx.λy.y")

if __name__ == "__main__":
    for i in [True, False]:
        print(lambda_to_bool(NOT(bool_to_lambda(i))))
    for i in [True, False]:
        for j in [True, False]:
            print(
                f"{i} AND {j} = {lambda_to_bool(AND(bool_to_lambda(i))(bool_to_lambda(j)))}"
            )
    for i in [True, False]:
        for j in [True, False]:
            print(
                f"{i} OR {j} = {lambda_to_bool(OR(bool_to_lambda(i))(bool_to_lambda(j)))}"
            )
    zero = parser("λf.λx.x")
    one = parser("λf.λx.(f x)")
    print(IF(bool_to_lambda(True))(one)(zero))
    print(IF(bool_to_lambda(False))(one)(zero))
