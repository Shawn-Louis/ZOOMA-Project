import uuid 
import datetime 
class Employee: 
    def __init__ (self, name, address):
        self.employee_id = str(uuid.uuid4()) 
        self.name = name 
        self.animals = []
        self.address = address

    def care(self,animal):
        self.animals.append(animal)
        

    def takeOver(self,animals):
        for animal in animals:
            self.animals.append(animal)
