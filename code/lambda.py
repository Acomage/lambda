
class Lambda:
    def __init__(self):
        pass
    def show(self):
        pass
    def replace(self):
        pass
class Variable(Lambda):
    def __init__(self, name:str):
        self.name = name 
    def show(self):
        return self.name
    def replace(self, to_be_replaced:Variable, replacement:Lambda):
        if self.name == to_be_replaced.name:
            self = replacement
class A

        
    

