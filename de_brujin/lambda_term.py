import copy
from abc import ABC, abstractmethod


class LambdaTerm(ABC):
    def __init__(self):
        self.is_normal = False

    @abstractmethod
    def __copy__(self) -> "LambdaTerm":
        pass

    @abstractmethod
    def show(self) -> str:
        pass

    @abstractmethod
    def de_bruijn_text(self) -> str:
        pass

    @abstractmethod
    def shift(self, d: int, c: int = 0):
        pass

    @abstractmethod
    def substitute(self, term: "LambdaTerm", depth: int = 0) -> "LambdaTerm":
        pass

    @abstractmethod
    def beta_reduce(self) -> "LambdaTerm":
        pass

    def super_beta_reduce(self) -> "LambdaTerm":
        temp = self.beta_reduce()
        while not temp.is_normal:
            temp = temp.beta_reduce()
        return temp

    @abstractmethod
    def final_equal(self, other: "LambdaTerm") -> bool:
        pass

    def __eq__(self, other: "LambdaTerm") -> bool:
        a_reduced = self.super_beta_reduce()
        b_reduced = other.super_beta_reduce()
        return a_reduced.final_equal(b_reduced)

    def __str__(self) -> str:
        temp = self.super_beta_reduce()
        return temp.show()

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, other: "LambdaTerm") -> "LambdaTerm":
        return Application(copy.copy(self), copy.copy(other))


class Variable(LambdaTerm):
    def __copy__(self):
        return Variable(self.name, self.index)

    def __init__(self, name: str, index: int = -1):
        self.name = name
        self.index = index
        self.is_normal = True

    def show(self) -> str:
        return self.name

    def de_bruijn_text(self) -> str:
        return str(self.index)

    def shift(self, d: int, c: int = 0):
        if self.index >= c:
            self.index += d

    def substitute(self, term: "LambdaTerm", depth: int = 0) -> "LambdaTerm":
        if self.index == depth:
            return copy.copy(term)
        return self

    def beta_reduce(self) -> "LambdaTerm":
        return self

    def final_equal(self, other: "LambdaTerm") -> bool:
        if isinstance(other, Variable):
            return self.name == other.name
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name

    def __str__(self) -> str:
        return self.name


class Abstraction(LambdaTerm):
    def __copy__(self):
        return Abstraction(self.var, self.body.__copy__())

    def __init__(self, var: Variable, body: LambdaTerm):
        super().__init__()
        self.var = var
        self.body = body

    def show(self) -> str:
        return f"λ{self.var.show()}.{self.body.show()}"

    def de_bruijn_text(self) -> str:
        return f"λ.{self.body.de_bruijn_text()}"

    def shift(self, d: int, c: int = 0):
        self.body.shift(d, c + 1)

    def substitute(self, term: "LambdaTerm", depth: int = 0) -> "LambdaTerm":
        # term.shift(1, 0)
        # self.body = self.body.substitute(term, depth + 1)
        # term.shift(-1, 1)
        # return self
        temp = copy.copy(term)
        temp.shift(1, 0)
        self.body = self.body.substitute(temp, depth + 1)
        return self

    def beta_reduce(self) -> "LambdaTerm":
        if self.body.is_normal:
            self.is_normal = True
            return self
        self.body = self.body.beta_reduce()
        return self

    def final_equal(self, other: "LambdaTerm") -> bool:
        if isinstance(other, Abstraction):
            return self.de_bruijn_text() == other.de_bruijn_text()
        else:
            return False


class Application(LambdaTerm):
    def __copy__(self):
        return Application(self.left.__copy__(), self.right.__copy__())

    def __init__(self, left: LambdaTerm, right: LambdaTerm):
        super().__init__()
        self.left = left
        self.right = right

    def show(self) -> str:
        if isinstance(self.left, Abstraction):
            return f"(({self.left.show()}) {self.right.show()})"
        return f"({self.left.show()} {self.right.show()})"

    def de_bruijn_text(self) -> str:
        return f"({self.left.de_bruijn_text()} {self.right.de_bruijn_text()})"

    def shift(self, d: int, c: int = 0):
        self.left.shift(d, c)
        self.right.shift(d, c)

    def substitute(self, term: "LambdaTerm", depth: int = 0) -> "LambdaTerm":
        self.left = self.left.substitute(term, depth)
        self.right = self.right.substitute(term, depth)
        return self

    def beta_reduce(self) -> "LambdaTerm":
        if isinstance(self.left, Abstraction):
            self.right.shift(1, 0)
            temp = self.left.body.substitute(self.right, 0)
            temp.shift(-1, 0)
            return temp
        else:
            if not self.left.is_normal:
                self.left = self.left.beta_reduce()
                return self
            elif not self.right.is_normal:
                self.right = self.right.beta_reduce()
                return self
            else:
                self.is_normal = True
                return self

    def final_equal(self, other: "LambdaTerm") -> bool:
        if isinstance(other, Application):
            return self.left.final_equal(other.left) and self.right.final_equal(
                other.right
            )
        else:
            return False


if __name__ == "__main__":
    from parser import parser

    f = parser("λx.λz.(λy.λw.(w y) x)")
    print(f.show())
    print(f.de_bruijn_text())
    f.super_beta_reduce()
