# import modules to interact with the file system
import sys
import os

# avail external project folder to this script, in order to import relevant module
sys.path.append(os.path.abspath(os.path.join('..')))

# import the module to be unit tested
import modules.analyser as analyser

# import relevant modules
import unittest 

class AttachmentTest (unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(analyser.Analyser)

    def test_has_ga_cases(self):
        anl = analyser.Analyser()
        self.assertIsNotNone(anl.ga_run_cases)
    
    def test_has_store_gen_data(self):
        self.assertIsNotNone(analyser.Analyser.store_gen_data)
    
    def test_store_data_local_storage(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 15, 15])
        self.assertGreater(len(anl.case_run_data), 0)

    def test_store_data_calcs_min_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 15, 15])
        self.assertEqual(anl.case_run_data[0]['case_name'], 'test')

    def test_store_data_calcs_min_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 15, 15])
        self.assertEqual(anl.case_run_data[0]['min_dist'], 10)

    def test_store_data_calcs_max_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 15, 15])
        self.assertEqual(anl.case_run_data[0]['max_dist'], 30)

    def test_store_data_calcs_mean_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 15, 15])
        self.assertEqual(anl.case_run_data[0]['mean_dist'], 20)

    def test_store_data_calcs_verts(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 7, 8])
        self.assertEqual(anl.case_run_data[0]['mean_verts'], 10)

    def test_store_data_sets_gen_num(self):
        anl = analyser.Analyser()
        anl.store_gen_data('test', [10, 20, 30], [15, 7, 8])
        anl.store_gen_data('test', [14, 40, 22], [9, 7, 12])
        anl.store_gen_data('test', [6, 55, 17], [13, 8, 8])
        self.assertEqual(anl.case_run_data[-1]['gen_num'], len(anl.case_run_data)-1)

unittest.main()