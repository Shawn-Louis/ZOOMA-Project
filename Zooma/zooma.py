from hashlib import new
from turtle import home
from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo
from enclosure import Enclosure
from animal import Animal 
from employee import Employee

my_zoo = Zoo()

zooma_app = Flask(__name__)
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)

enclosure_id_arg = 'enclosure_id'
mother_id_arg = 'mother_id'
animal_id_arg = 'animal_id'

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True, location='form', help='The scientific name of the animal, e,g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, location='form', help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, location='form', help='The age of the animal, e.g., 12')

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help='The name of the enclosure')
enclosure_parser.add_argument('area', type=int, required=True, help='The area within the zoo where the enclosure is located, e.g., 4')

home_parser = reqparse.RequestParser()
home_parser.add_argument(enclosure_id_arg, type=str, required=True)

birth_parser = reqparse.RequestParser()
birth_parser.add_argument(mother_id_arg, type=str, required=True)

death_parser = reqparse.RequestParser()
death_parser.add_argument(animal_id_arg, type=str, required=True)       

employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True, help='Name of a caretaker')
employee_parser.add_argument('address', type=str, required=True, help='Care takers address')

@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal (species, name, age) 
        #add the animal to the zoo
        my_zoo.addAnimal (new_animal) 
        return jsonify(new_animal) 
    

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result  = my_zoo.getAnimal(animal_id)
        return search_result # this is automatically jsonified by flask-restx
    
     def delete(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} was removed")     
     
@zooma_api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):
     def post(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found") 
        targeted_animal.feed()
        return jsonify(targeted_animal)

@zooma_api.route('/animal/<animal_id>/vet')
class AnimalCheckUp(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.medicalCheck()
        return jsonify(targeted_animal)
        
@zooma_api.route('/animals/<animal_id>/home')
class HomeAnimal(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        parsed_args = home_parser.parse_args()
        enclosure_id = parsed_args[enclosure_id_arg]
        animal  = my_zoo.getAnimal(animal_id)
        enclosure = my_zoo.getEnclosure(enclosure_id)

        if animal not in my_zoo.animals:
            return jsonify(f"Animal with id {animal_id} was not found")

        if enclosure not in my_zoo.enclosures:
            return jsonify(f"Animal with id {enclosure_id} was not found")
        
        my_zoo.addAnimalToEnclosure(animal,enclosure)
        return jsonify(animal)


@zooma_api.route('/animals')
class AllAnimals(Resource):
     def get(self):
        return jsonify( my_zoo.animals)

@zooma_api.route('/animals/birth')
class BirthAnimal(Resource):
    @zooma_api.doc(parser=birth_parser)
    def post(self):
        parsed_args = birth_parser.parse_args()
        mother_id = parsed_args[mother_id_arg]         
        mother  = my_zoo.getAnimal(mother_id)
        if not mother: 
            return jsonify(f"Animal with ID {mother_id} was not found")      
        child = mother.birth()
        mother_enclosure = my_zoo.getEnclosure(mother.enclosure)
        if not(mother_enclosure):
            return jsonify(f"Mother with ID {mother_id} has no enclosure")
        mother_enclosure.animals.append(child)            
        my_zoo.addAnimal (child)
        return jsonify(child)

@zooma_api.route('/animal/death')
class AnimalDie(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        parsed_args = death_parser.parse_args()
        animal_id = parsed_args["animal_id"]         
        animal  = my_zoo.getAnimal(animal_id)
        if animal not in my_zoo.animals: 
            return jsonify(f"Animal with ID {animal_id} was not found")         
        enclosure = my_zoo.getEnclosure(animal.enclosure)
        my_zoo.animalDeath(animal,enclosure) 
        
        animal.die()
        return jsonify(animal)

@zooma_api.route('/animals/stat')
class AnimalStats(Resource):
    def get(self):
        
        return jsonify(my_zoo.animalStats())

@zooma_api.route('/enclosure')
class AddEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']
        new_enclosure = Enclosure(name, area)
        my_zoo.addEnclosure (new_enclosure) 
        return jsonify(new_enclosure)

@zooma_api.route('/enclosures')
class Enclosures(Resource):
     def get(self):
        return jsonify(my_zoo.enclosures)  


@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
     def post(self, enclosure_id):
        enclosure  = my_zoo.getEnclosure(enclosure_id)
        if not(enclosure): 

            return jsonify(f"Enclosure with ID {enclosure_id} was not found") 
        my_zoo.cleanEnclosure()
        return jsonify(enclosure)

@zooma_api.route('/enclosures/<enclosure_id>/animals')
class EnclosureAnimals(Resource):
     def get(self,enclosure_id):
        enclosure  = my_zoo.getEnclosure(enclosure_id)
        if not(enclosure): 
            return jsonify(f"Enclosure with ID {enclosure_id} was not found") 
        return jsonify(enclosure.animals)  

@zooma_api.route('/enclosure/<enclosure_id>')
class Enclosure_Id(Resource):    
    def delete(self, enclosure_id):
        targeted_enclosure  = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure: 
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        my_zoo.removeEnclosure(targeted_enclosure)
        return jsonify(f"Enclosure with ID {enclosure_id} was removed") 


@zooma_api.route('/employee')
class AddEmployee(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):
        args = employee_parser.parse_args()
        address = args['address']
        name = args['name']  
        employee = Employee(name, address) 
        my_zoo.addEmployee(employee) 
        return jsonify(employee) 

employee_animal_parser = reqparse.RequestParser()
@zooma_api.route('/employee/<employee_id>/care/<animal_id>/')
class Care(Resource):
    
    def post(self,animal_id,employee_id):
        
        animal  = my_zoo.getAnimal(animal_id) 
        if not(animal): 
            return jsonify(f"Animal with ID {animal_id} was not found")
        
        employee = my_zoo.getEmployee(employee_id)
        
        if animal.care_taker: 
            return jsonify(f"Animal with ID {animal_id} already has a caretaker (ID: {employee_id})")
         
        if not(employee): 
            return jsonify(f"Employee with ID {employee_id} was not found") 
        employee.care(animal)
        animal.care_taker = employee.name
        return jsonify(employee)

@zooma_api.route('/employee/<employee_id>/care/animals')
class GetSupervisedAnimalsList(Resource):
     def get(self,employee_id):
        employee  = my_zoo.getEmployee(employee_id)
        if not(employee): 
            return jsonify(f"Employee with ID {employee_id} was not found") 
        return jsonify(employee.animals)  

@zooma_api.route('/employee/<employee_id>')
class Employeet(Resource):
    
    def delete(self,employee_id):
        if len(my_zoo.employees)<2:
            return jsonify(f"There has to be more than 1 employee before you can delete any.")
        employeet  = my_zoo.getEmployee(employee_id)
        new_employee = my_zoo.getRandomEmployee()
        animals = employeet.animals
        if not(employeet): 
            return jsonify(f"Employee with ID {employee_id} was not found") 
        
        new_employee.takeOver(animals)
        for animal in animals:
            animal.care_taker = new_employee
            
            
        my_zoo.kickEmployee(employeet)
        return jsonify(new_employee)

@zooma_api.route('/employees/stats')
class EmployeeStats(Resource):
     def get(self):
        return jsonify(my_zoo.stats())  

@zooma_api.route('/tasks/medical/')
class Medical_plan(Resource):
     def get(self):

        return jsonify(my_zoo.medical())  
    

@zooma_api.route('/tasks/cleaning/')
class CleaningPlan(Resource):
     def get(self):

        return jsonify(my_zoo.cleaning())  

@zooma_api.route('/tasks/feeding/')
class FeedingPlan(Resource):
     def get(self):

        return jsonify(my_zoo.feeding())  

if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)

