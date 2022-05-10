import random
import datetime

class Zoo: 
    def __init__ (self): 
        self.animals = []
        self.enclosures = []
        self.dead_animals = []
        self.employees = []
        
    def addAnimal(self, animal): 
        self.animals.append (animal) 
        
    def removeAnimal(self, animal): 
        self.animals.remove(animal) 
    
    def getAnimal(self, animal_id): 
        for animal in self.animals: 
            if animal.animal_id == animal_id: 
                return animal
        
    def addEnclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def removeEnclosure(self, enclosure):
        self.enclosures.remove(enclosure)

    def getEnclosure(self, enclosure_id): 
        for enclosure in self.enclosures: 
            if enclosure.enclosure_id == enclosure_id: 
                return enclosure        

    def addAnimalToEnclosure(self, animal, enclosure):
        enclosure.animals.append(animal)
        animal.enclosure = enclosure.enclosure_id

    def cleanEnclosure(self,enclosure_id):
        for enclosure in self.enclosures:     
            if enclosure.name == enclosure_id:
                enclosure.cleaning_records.append(datetime.datetime.now())


    def animalDeath(self, animal, enclosure):
        if animal.enclosure:
            enclosure.removeAnimal(animal.animal_id)
        animal.isDead = True
        self.animals.remove(animal)
        self.dead_animals.append(animal)

    def addEmployee(self, employee):
        self.employees.append(employee)

    def getEmployee(self, employee_id): 
        for employee in self.employees: 
            if employee.employee_id == employee_id: 
                return employee        

    def getRandomEmployee(self):
        return self.employees[random.randint(0, len(self.employees) - 1)]

    def kickEmployee(self, employee):
        self.employees.remove(employee)


    def animalStats(self):
        num_per_species = {}
        if not(self.animals):
            return "there are no animals in the list"
        for x in self.animals:
            if x.species_name in num_per_species:
                num_per_species[x.species_name] +=1
            else:
                num_per_species[x.species_name] = 1
        
        animals = []
        
        if not(self.enclosures):
            return "there are no enclosures in the list"          
        for x in self.enclosures:
            animals.append(len(x.animals))

        avg_per_enclosure = sum(animals)/len(self.enclosures)
        enclosure_space = {}
        for x in self.enclosures:
            enclosure_space[x.name] =(int(x.area))/(int(len(x.animals)))

        return f"Number of animals per species: {num_per_species}; Average animals per Enclosure = {avg_per_enclosure}; Avg area occupied per enclosure:{enclosure_space}"

    def stats(self):
        num_animals = []
        for employee in self.caretakers:
            num_animals.append(len(employee.animals))

        min_ = min(num_animals)
        avg_ = sum(num_animals)/len(num_animals)
        max_ = max(num_animals)
        
        return f"Minimum animals under supervision: {min_}; Average: {avg_}; Max: {max_}"

    def medical(self):       
        for animal in self.animals:
            if len(animal.medical_checkup)>0:
                last_checkup = animal.medical_checkup[-1]
            else:
                last_checkup = datetime.datetime.now()     
            month = last_checkup.month
            day = last_checkup.day
            next_month = int(month)+1
            if day<(31-7):
                next_day = day+7
            else:
                next_month+=1
                next_day = 7-(31-day)
        
        return f"Month:{next_month} Day:{next_day}"

    
    def cleaning(self):
        if len(self.enclosures) ==0:
            return "there are no enclosures"
        if len(self.employees) ==0:
            return "there are no employees"
        for  enclosure in self.enclosures:
            if len(enclosure.cleaning_record)>0:
                last_cleaned = enclosure.cleaning_record[-1]       
            else:
                last_cleaned = datetime.datetime.now()       
                month =last_cleaned.month
                day = last_cleaned.day
                next_month = int(month)
                if day<(31-3):
                    next_cleanday = day+3
                else:
                    next_month+=1
                    next_cleanday = 3-(31-day)

                person =random.randrange(0,len(self.employees))

        return f"Month:{next_month} Day:{next_cleanday} Responsible person {self.employees[person].name}"


    def feeding(self):
        if len(self.animals) ==0:
            return "there are no animals in the list"
        
        for  animal in self.animals:
            if animal.care_taker == None:
                return f"Animal {animal.animal_id} does not have a caretaker. Provide a caretaker before feeding"
            if len(animal.feeding_record)>0:
                last_fed = animal.feeding_record[-1]
            else:
                last_fed = datetime.datetime.now()
            
            month =last_fed.month
            day = last_fed.day
            next_month = int(month)
            if day<(31-2):
                next_feed = day+2
            else:
                next_month+=1
                next_feed = 2-(31-day)


        return f"Month:{next_month} Day:{next_feed} Responsible person {animal.care_taker}"

