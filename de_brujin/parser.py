from typing import List, Tuple
from lark import Lark, Transformer, v_args
from lambda_term import LambdaTerm, Variable, Abstraction, Application

lambda_grammar = """
    %import common.WS
    %ignore WS
    ?start: expr
    ?expr: variable
        | application
        | abstraction
        | "(" expr ")"
    variable: /[a-z]+[0-9]*/
    abstraction: "λ" variable "." expr
    application: expr (variable | abstraction | "(" expr ")")
"""


class LambdaTransformer(Transformer):
    def variable(self, var):
        return {"type": "variable", "name": var[0].value}

    def abstraction(self, abs):
        return {"type": "abstraction", "var": abs[0], "body": abs[1]}

    @v_args(inline=True)
    def application(self, *args):
        return {"type": "application", "left": args[0], "right": args[1]}


lambda_parser = Lark(lambda_grammar, parser="lalr", transformer=LambdaTransformer())
parse = lambda_parser.parse


def parse_expression(expr: str) -> Tuple["LambdaTerm", List["Variable"]]:
    tree = parse(expr)
    return parse_tree(tree)


def parse_tree(tree: dict) -> Tuple["LambdaTerm", List["Variable"]]:
    # print(tree)
    if tree["type"] == "variable":
        variable = Variable(tree["name"])
        return variable, [variable]
    elif tree["type"] == "abstraction":
        var = Variable(tree["var"]["name"])
        body, body_free = parse_tree(tree["body"])
        free = body_free.copy()
        for free_var in body_free:
            free_var.index += 1
            if free_var.name == var.name:
                free.remove(free_var)
        return Abstraction(var, body), free
    elif tree["type"] == "application":
        left, left_free = parse_tree(tree["left"])
        right, right_free = parse_tree(tree["right"])
        free = left_free + right_free
        return Application(left, right), free
    else:
        raise ValueError("Invalid expression")


def parser(expr: str, close: bool = True) -> "LambdaTerm":
    lambda_term, free = parse_expression(expr)
    if close:
        if free:
            raise ValueError(f"Free variables in the expression: {free}")
    return lambda_term
