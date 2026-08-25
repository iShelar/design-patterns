# Not a good example for decorator pattern.

from abc import ABC, abstractmethod

# Abstract Class
class Beverage(ABC):
    @abstractmethod
    def get_description(self) -> str:
        ...
    
    @abstractmethod
    def cost(self) -> float:
        ...

# Concrete Classes
class Decaf(Beverage):
    def __init__(self) -> None:
        self.price = 2.99
    def get_description(self) -> str:
        return f"Decaf: {self.price}"
    
    def cost(self) -> float:
        return self.price

class Espresso(Beverage):
    def __init__(self) -> None:
        self.price = 3.99
    def get_description(self) -> str:
        return f"Espresso: {self.price}"
    
    def cost(self) -> float:
        return self.price

# Decorator Class

class AddonsDecorator(Beverage):
    @abstractmethod
    def get_description(self) -> str:
        ...
    @abstractmethod
    def cost(self) -> float:
        ...

# Addons
class Caramel(AddonsDecorator):
    def __init__(self, beverage: Beverage) -> None:
        self.beverage = beverage
        self.price = 1.49
    
    def get_description(self) -> str:
        return f"{self.beverage.get_description()} Caramel: {self.price}"

    def cost(self) -> float:
        return self.beverage.cost() + self.price

class Soy(AddonsDecorator):
    def __init__(self, beverage: Beverage) -> None:
        self.beverage = beverage
        self.price = 1.29
    
    def get_description(self) -> str:
        return f"{self.beverage.get_description()} Soy: {self.price}"

    def cost(self) -> float:
        return self.beverage.cost() + self.price


beverage = Soy(Espresso())
print(f"{beverage.get_description()} | Cost: {beverage.cost()}")
    
