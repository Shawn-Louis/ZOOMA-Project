import uuid 
import datetime 
class Enclosure: 
    def __init__ (self, name, area):
        self.enclosure_id = str(uuid.uuid4()) 
        self.name = name 
        self.area = area 
        self.animals = []
        self.cleaning_record = []
        # add more as required here 

    def removeAnimal(self,animal_id):
        self.animals.remove(animal_id)

    def clean(self):
        self.cleaning_record.append(f"Enclosure cleaned at {datetime.datetime.now()}")


    def takeResponsibility(self,animals_list):
        for x in animals_list:
            self.animals.append(x)