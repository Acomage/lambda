
class Lambda:
    def __init__(self):
        pass
    def show(self):
        pass
    def replace(self):
        pass
    def alpha_convert(self):
        pass
    def beta_reduce(self):
        pass
      
class Variable(Lambda):
    def __init__(self, name:str):
        self.name = name 
    def show(self):
        return self.name
    def replace(self, to_be_replaced:'Variable', replacement:Lambda)->Lambda:
        if self.name == to_be_replaced.name:
            return replacement 
        else:
            return self
    def alpha_convert(self, new_name:str)->'Variable':
        return Variable(new_name)
    def beta_reduce(self):
        return self


class Abstraction(Lambda):
    def __init__(self, variable:Variable, body:Lambda):
        self.variable = variable
        self.body = body
    def show(self):
        return f'λ{self.variable.show()}.{self.body.show()}'
    def replace(self, to_be_replaced:Variable, replacement:Lambda)->Lambda:
        return Abstraction(self.variable.replace(to_be_replaced, replacement), self.body.replace(to_be_replaced, replacement))
    def alpha_convert(self, new_name:str)->Lambda:
        return Application(self.variable.alpha_convert(new_name), self.body.replace(self.variable, Variable(new_name)))
    def beta_reduce(self)->Lambda:
        return Abstraction(self.variable, self.body.beta_reduce())

class Application(Lambda):
    def __init__(self, left:Lambda, right:Lambda):
        self.left = left
        self.right = right
    def show(self):
        return f'({self.left.show()} {self.right.show()})'
    def replace(self, to_be_replaced, replacement)->Lambda:
        return Abstraction(self.left.replace(to_be_replaced, replacement), self.right.replace(to_be_replaced, replacement))
    def alpha_convert(self, new_name:str)->Lambda:
        return self
    def beta_reduce(self)->Lambda:
        if isinstance(self.left, Abstraction):
            return (self.left.body.replace(self.left.variable, self.right)).beta_reduce()
        else:
            return Application(self.left.beta_reduce(), self.right.beta_reduce())

Successor = Abstraction(Variable('n'), Abstraction(Variable('f'), Abstraction(Variable('x'), Application(Variable('f'), Application(Application(Variable('n'), Variable('f')), Variable('x'))))))
Zero = Abstraction(Variable('x'), Variable('x'))


if  __name__ == '__main__':
    print(Zero.show())
    print(Successor.show())
    print(Application(Successor, Zero).show())
    print(Application(Successor, Zero).beta_reduce().show())
    print(Application(Zero, Variable('f')).beta_reduce().show())


