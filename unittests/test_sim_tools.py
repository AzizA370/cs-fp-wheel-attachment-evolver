# import modules to interact with the file system
import sys
import os

# avail external project folder to this script, in order to import relevant module
sys.path.append(os.path.abspath(os.path.join('..')))

# import the module to be unit tested
import modules.sim_tools as sim_tools

# import relevant modules
import unittest 

class SimToolsTest (unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(sim_tools.SimTools)
    
    def test_create_circle_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.create_circle)
    
    def test_random_connect_Verts_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.connect_vert_to_vert)
    
    def test_build_chasis_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.build_chasis)
    
    def test_set_motors_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.set_motors)
    
    def test_create_stairs_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.create_stairs)
    
    def test_create_boundries_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.create_boundries)

    def test_construct_vehicle_exists(self):
        self.assertIsNotNone(sim_tools.SimTools.construct_vehicle)
    
    

unittest.main()