# import modules to interact with the file system
import sys
import os

# avail external project folder to this script, in order to import relevant module
sys.path.append(os.path.abspath(os.path.join('..')))

# import the module to be unit tested
import modules.simulation as simulation
import modules.attachment as attachment
import modules.genome as genome

import unittest 

class SimulationTest (unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(simulation.Simulation)
    
    def test_draw_exists(self):
        self.assertIsNotNone(simulation.Simulation.draw)
    
    def test_run_wheel_exists(self):
        self.assertIsNotNone(simulation.Simulation.run_wheel)
    
    def test_running_simulation(self):
        sim = simulation.Simulation()
        attach = attachment.Attachment(gene_count=10)
        sim.run_wheel(attach, speed=2.0)
        self.assertIsNotNone(sim)
    
    def test_pos_updates(self): 
        sim = simulation.Simulation()
        attach = attachment.Attachment(gene_count=10)
        sim.run_wheel(attach, speed=1.0, iterations=2900)
        self.assertNotEqual(attach.initial_position, attach.final_position)
    
unittest.main()