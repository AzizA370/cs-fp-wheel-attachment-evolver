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
        anl.load_cases_from_json('test_case.json')
        self.assertIsNotNone(anl.ga_run_cases)
    
    def test_load_cases_from_json_exists(self):
        self.assertIsNotNone(analyser.Analyser.load_cases_from_json)
    
    def test_load_cases_from_json_loads_cases(self):
        anl = analyser.Analyser()
        anl.load_cases_from_json('test_case.json')
        self.assertIsNotNone(anl.ga_run_cases)

    def test_store_gen_data_exists(self):
        self.assertIsNotNone(analyser.Analyser.store_gen_data)
    
    def test_store_data_local_storage(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 15, 15], [[11],[22],[33], [44]])
        self.assertGreater(len(anl.case_run_data), 0)

    def test_store_data_calcs_min_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 15, 15], [[11],[22],[33], [44]])
        self.assertEqual(anl.case_run_data[0]['case_name'], 'test')

    def test_store_data_calcs_min_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 15, 15], [[11],[22],[33], [44]])
        self.assertEqual(anl.case_run_data[0]['min_dist'], 10)

    def test_store_data_calcs_max_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 15, 15], [[11],[22],[33], [44]])
        self.assertEqual(anl.case_run_data[0]['max_dist'], 30)

    def test_store_data_calcs_mean_fit(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 15, 15], [[11],[22],[33], [44]])
        self.assertEqual(anl.case_run_data[0]['mean_dist'], 20)

    def test_store_data_calcs_verts(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 7, 8], [[11],[22],[33], [44]])
        self.assertEqual(anl.case_run_data[0]['mean_verts'], 10)

    def test_store_data_sets_gen_num(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 7, 8], [[11],[22],[33], [44]])
        anl.store_gen_data([14, 40, 22], [9, 7, 12], [[11],[22],[33], [44]])
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        self.assertEqual(anl.case_run_data[-1]['gen_num'], len(anl.case_run_data)-1)

    def test_process_case_data_exists(self):
        self.assertIsNotNone(analyser.Analyser.process_case_data)

    def test_create_case_csv_exists(self):
        self.assertIsNotNone(analyser.Analyser.create_case_csv)

    def test_create_case_csv_output(self):
        anl = analyser.Analyser()
        anl.store_gen_data([10, 20, 30], [15, 7, 8], [[11],[22],[33], [44]])
        file_path = '../cases_analytics/test_case/test_case.csv'
        anl.create_case_csv(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_create_case_plots_exists(self):
        self.assertIsNotNone(analyser.Analyser.create_case_plots)

    def test_create_case_plots_sets_folder(self):
        anl = analyser.Analyser()
        anl.load_cases_from_json('test_case.json')
        file_path = '../cases_analytics/test_case/test_plots'
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.create_case_plots(file_path, 'test_case')
        self.assertTrue(os.path.exists(file_path))

    def test_elites_to_csv_exists(self):
        self.assertIsNotNone(analyser.Analyser.elites_to_csv)

    def test_elites_to_csv_sets_folder(self):
        anl = analyser.Analyser()
        file_path = '../cases_analytics/test_case/test_elite'
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.elites_to_csv(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_draw_best_shape_exists(self):
        self.assertIsNotNone(analyser.Analyser.draw_best_shape)

    def test_draw_best_shape_creates_graphic(self):
        anl = analyser.Analyser()
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        anl.store_gen_data([6, 55, 17], [13, 8, 8], [[11],[22],[33], [44]])
        file_path = '../cases_analytics/test_case/test_plots'
        anl.draw_best_shape(file_path)
        self.assertTrue(os.path.exists(file_path))

unittest.main()