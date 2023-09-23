# import modules to interact with the file system
import sys
import os

# avail external project folder to this script, in order to import relevant module
sys.path.append(os.path.abspath(os.path.join('..')))

# import the module to be unit tested
import modules.genome as genome

# import relevant modules
import unittest 
import numpy as np

class GenomeTest (unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(genome.Genome)

    def test_random_gene_exists(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def test_random_gene_is_numpy_array(self):
        random_gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(random_gene), np.ndarray)

    def test_random_gene_length(self):
        random_gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(random_gene), 20)

    def test_random_genome_exists(self):
        self.assertIsNotNone(genome.Genome.get_random_genome)

    def test_random_genome_is_numpy_arrays(self):
        random_genome = genome.Genome.get_random_genome(10, 20)
        self.assertEqual(type(random_genome), list)

    def test_random_genome_length(self):
        random_genome = genome.Genome.get_random_genome(10, 20)
        self.assertEqual(len(random_genome), 20)

    def test_genome_spec_exists(self):
        self.assertIsNotNone(genome.Genome.get_gene_spec)

    def test_gene_spec_has_vert_dist(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['vert_dist'])

    def test_gene_spec_has_vert_sist_index(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['vert_dist']['ind'])

    def test_gene_spec_scale(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 5)
        self.assertGreater(dna[0][spec['vert_dist']['ind']], 0)

    def test_gene_dict_exists(self):
        self.assertIsNotNone(genome.Genome.get_gene_dict)

    def test_genome_dicts_exists(self):
        self.assertIsNotNone(genome.Genome.get_genome_dicts)
    
    def test_genome_to_genome_dicts_holds_specs(self):
        
        spec = genome.Genome.get_gene_spec()

        dna = genome.Genome.get_random_genome(len(spec), 5)
        
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        
        self.assertIn('vert_dist', genome_dicts[0])
    
    def test_uniform_crossover_exists(self):
        self.assertIsNotNone(genome.Genome.uniform_crossover)

    def test_uniform_crossover_output(self):
        g1 = np.array([[1,3], [4,6], [7, 9], [10, 12], [13, 15]])
        g2 = np.array([[71, 3], [74,75], [77, 79]])
        g3 = genome.Genome.uniform_crossover(g1, g2)
        avg_length = (len(g1) + len(g2))/2
        self.assertGreaterEqual(len(g3), avg_length)

    def test_point_mutation_exists(self):
        self.assertIsNotNone(genome.Genome.point_mutate)

    def test_point_mutation_output(self):
        g1 = np.array([[0.14, 0.22], [0.45, 0.56], 
                        [0.65, 0.78], [0.89, 0.90], [0.12, 0.13]])
    
        new_genome = genome.Genome.point_mutate(g1, 1, 0.25)
        self.assertNotEqual(g1[0][0], new_genome[0][0])

    def test_shrink_mutation_exists(self):
        self.assertIsNotNone(genome.Genome.shrink_mutate)

    def test_shrink_mutation_output(self):
        g1 = np.array([[0.14, 0.22], [0.45, 0.56], 
                        [0.65, 0.78], [0.89, 0.90], [0.12, 0.13]])
        
        new_genome = genome.Genome.shrink_mutate(g1, 1.0)
        self.assertLess(len(new_genome), len(g1))

    def test_grow_mutation_exists(self):
        self.assertIsNotNone(genome.Genome.grow_mutate)

    def test_grow_mutation_output(self):
        g1 = np.array([[0.14, 0.22], [0.45, 0.56], 
                        [0.65, 0.78], [0.89, 0.90], [0.12, 0.13]])
        
        new_genome = genome.Genome.grow_mutate(g1, 1)
        self.assertGreater(len(new_genome), len(g1))

    def test_swap_mutation_exists(self):
        self.assertIsNotNone(genome.Genome.swap_mutate)

    def test_swap_mutation_output(self):
        g1 = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]])
        new_genome = genome.Genome.swap_mutate(g1, 1)
        self.assertEqual(len(g1), len(new_genome))
        
    
    def test_scramble_mutation_exists(self):
        self.assertIsNotNone(genome.Genome.scramble_mutate)

    def test_scramble_mutation_output(self):
        g1 = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]])
        subset_prop = 0
        new_genome = genome.Genome.scramble_mutate(g1, 1, subset_prop)

        self.assertEqual(len(g1), len(new_genome))
        
    def test_inversion_mutation_exists(self):
        self.assertIsNotNone(genome.Genome.invert_mutate)

    def test_inversion_mutation_output(self):
        g1 = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]])
        subset_prop = 0.3
        new_genome = genome.Genome.invert_mutate(g1, 1, subset_prop)
        self.assertEqual(len(g1), len(new_genome))

    def test_to_csv_exists(self):
        self.assertIsNotNone(genome.Genome.to_csv)

    def test_to_csv_generates_file(self):
        g1 = [[1,2,3], [4,5,6]]
        file_path = 'test_CSVs/test1.csv'
        genome.Genome.to_csv(g1, file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_to_csv_output_content(self):
        g1 = [[1,2,3], [4,5,6], [7, 8, 9]]
        file_path = 'test_CSVs/test2.csv'
        genome.Genome.to_csv(g1, file_path)
        expected_content = "1,2,3,\n4,5,6,\n7,8,9,\n"
        with open(file_path) as f:
            csv_str = f.read() 
        self.assertEqual(csv_str, expected_content)

    def test_from_csv_exists(self):
        self.assertIsNotNone(genome.Genome.from_csv)

    def test_from_csv_input(self):
        g1 = [[1,2,3]]
        file_path = 'test_CSVs/test3.csv'
        genome.Genome.to_csv(g1, file_path)
        g2 = genome.Genome.from_csv(file_path)
        self.assertTrue(np.array_equal(g1, g2))

    def test_from_csv_input_long(self):
        g1 = [[1,2,3], [4,5,6], [7, 8, 9]]
        file_path = 'test_CSVs/test4.csv'
        genome.Genome.to_csv(g1, file_path)
        g2 = genome.Genome.from_csv(file_path)
        self.assertTrue(np.array_equal(g1, g2))

unittest.main()