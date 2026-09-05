# Oops concepts implementation

class Car:
    def __init__(self,brand,speed):
        self.brand=brand
        self.speed=speed

    def accelerate(self,amount):
        self.speed+=amount

    def __str__(self):
        return f'Car brand is {self.brand} is moving at speed {self.speed}'

car1=Car("BMW",200)
car1.accelerate(50)
print(car1)

# Encapsulation
class BankAccount:
    def __init__(self,balance):
        self._balance=balance
        self.__pin="1234"

    def deposite(self,amount):
        if(amount<=0):
            return ValueError("Deposite amount must be grater than zero")
        self._balance+=amount

    @property
    def get_balence(self):
        return self._balance

    def __str__(self):
        return f'Account holds {self._balance} this amount currently'


account=BankAccount(1252800)
account.deposite(12345)
print(account.get_balence)


#Abstraction
class CoffeShop:
    def make_coffe(self):
        self._heat_water()
        self._add_powder()
        self._brew()
        return "Coffe ready!!!"

    def _heat_water(self):
        pass
    def _add_powder(self):
       pass
    def _brew(self):
        pass

machines=CoffeShop()
print(machines._heat_water())


# Inheritance
class Animal:
    def __init__(self,name):
        self.name=name
    def speak(self):
        return "Hii I Am Animal"

class Dog(Animal):
    def speak(self):
        return f"i am barking {self.name} Eyyyyy"

class Cat(Animal):
    def speak(self):
        return f"i am meoww {self.name} meowww"

animals=[Dog("Fahh"),Cat("Ahaa")]
for i in animals:
    print(i.speak())

class Employee:
    def __init__(self,name,age,salary):
        self.name=name
        self.age=age
        self.salary=salary

class Manager(Employee):
    def __init__(self,name,age,salary,experience):
        super().__init__(name,age,salary)
        self.experience=experience


# Polymorphisim
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    print(shape.area())   
    

class Book:
    total_books = 0                       

    def __init__(self, title):
        self.title = title
        Book.total_books += 1

    def describe(self):                    
        return f"Book: {self.title}"

    @classmethod
    def from_string(cls, data_string):     
        title = data_string.split(",")[0]
        return cls(title)                   

    @staticmethod
    def is_valid_title(title):             
        return len(title) > 0

b = Book.from_string("Dune,Frank Herbert")
print(Book.is_valid_title("Dune"))          
print(Book.total_books)
