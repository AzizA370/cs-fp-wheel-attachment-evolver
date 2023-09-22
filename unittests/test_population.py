# import modules to interact with the file system
import sys
import os

# avail external project folder to this script, in order to import relevant module
sys.path.append(os.path.abspath(os.path.join('..')))

# import the module to be unit tested
import modules.population as population

# import relevant modules
import unittest
import numpy as np

class TestPop(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(population.Population)

    def test_class_holds_vehicles(self):
        pop = population.Population(10, 30)
        self.assertEqual(len(pop.attachments), 10)

    def test_pop_elements_are_accessible(self):
        pop = population.Population(10, 30)
        pop.attachments[0].get_wheel_specs()
        self.assertIsNotNone(pop.attachments[0].wheel_specs)
        
    def test_selected_parent(self):
        fits = [2.5, 1.2, 3.4]
        fitmap = population.Population.get_fitness_map(fits)
        parent_ind = population.Population.select_parent(fitmap)
        self.assertLess(parent_ind, 3)

    def test_selected_parent_2(self):
        fits = [0, 1000, 0.1]
        fitmap = population.Population.get_fitness_map(fits)
        parent_ind = population.Population.select_parent(fitmap)
        self.assertEqual(parent_ind, 1)    

unittest.main()