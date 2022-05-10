import pytest
from animal import *
from enclosure import *
from zoo import *

def test_dead_animal_in_appropriate_list():
    test_zoo = Zoo()
    animal = Animal("Lab rat", "Steve", "2")
    test_zoo.addAnimal(animal)
    test_enclosure = Enclosure("Test lab", "999")
    test_enclosure.animals.append(animal.animal_id)

    test_zoo.animalDeath(animal, test_enclosure)
    animal.die()

    assert animal.isDead
    assert animal in test_zoo.dead_animals
