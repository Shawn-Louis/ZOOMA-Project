import uuid 
import datetime 
class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = [] 
        self.enclosure = None 
        self.care_taker = None 
        self.checkup_record = []
        self.isDead = False
        
    def feed(self): 
        self.feeding_record.append ( datetime.datetime.now()) 

    def medicalCheck(self):
        self.checkup_record.append(f"Checkup complete at {datetime.datetime.now()}")

    # There are 150 better ways to implement this but I would rather keep it as-is just for the memes.
    def die(self):
        self.isDead = True

    def birth(self):
        child = Child(self)
        return child

class Child(Animal):
    def __init__(self,motherAnimal):
        self.animal_id = str(uuid.uuid4())
        self.age = 0
        self.feeding_record = [] 
        self.care_taker = None 
        self.medical_checkup = []
        self.common_name = motherAnimal.common_name
        self.species_name = motherAnimal.species_name
        self.enclosure = motherAnimal.enclosure
        self.motherID = motherAnimal.animal_id

