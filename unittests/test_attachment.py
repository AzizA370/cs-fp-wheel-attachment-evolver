# import modules to interact with the file system
import sys
import os

# avail external project folder to this script, in order to import relevant module
sys.path.append(os.path.abspath(os.path.join('..')))

# import the module to be unit tested
import modules.attachment as attachment

# import relevant modules
import modules.genome as genome
import unittest 
import numpy as np

class AttachmentTest (unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(attachment.Attachment)
    
    def test_set_vertices_coordinates_exists(self):
        self.assertIsNotNone(attachment.Attachment.set_vertices_coordinates)

    def test_set_vertices_coordinates_output(self):
        attachm = attachment.Attachment(10)
        spec = attachm.spec
        dna = attachm.dna
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        verts_pos = attachment.Attachment.set_vertices_coordinates(500, 600, genome_dicts)
        self.assertIsNotNone(verts_pos)

    def test_get_clockwise_adjacency_exists(self):
        self.assertIsNotNone(attachment.Attachment.get_clockwise_adjacency)

    def test_get_clockwise_output(self):
        coords = np.array([[19, 89], [100,400], [88,190], [230,63], 
                            [17,105],[130,320], [49,36], [246, 95]])
        sorted_coords = attachment.Attachment.get_clockwise_adjacency(coords)
        self.assertEqual(len(coords), len(sorted_coords))

    def test_set_attachment_verts_exists(self):
        self.assertIsNotNone(attachment.Attachment.set_attachment_vertices)

    def test_set_attachment_vertices_vert_Pos_output(self):
        attachm = attachment.Attachment(10)
        attachm.set_attachment_vertices()
        self.assertGreater(len(attachm.vertices_pos), 0)

    def test_setup_attachment_exists(self):
        self.assertIsNotNone(attachment.Attachment.setup_attachment)

    def test_setup_attachment_sets_attachment(self):
        attachm = attachment.Attachment(10)
        attachm.set_attachment_vertices()
        attachm.setup_attachment()
        self.assertIsNotNone(attachm.attachment_a)
    
    def test_setup_attachment_sets_attachment_siblings(self):
        attachm = attachment.Attachment(10)
        attachm.set_attachment_vertices()
        attachm.setup_attachment()
        self.assertIsNotNone(attachm.attachment_a['vertices'][0]['sibling_a'])

    def test_set_attachment_offset_exists(self):
        self.assertIsNotNone(attachment.Attachment.set_attachment_offset)

    def test_set_attachment_offset_sets_second_attachment(self):
        attachm = attachment.Attachment(10)
        attachm.set_attachment_vertices()
        attachm.setup_attachment()
        attachm.set_attachment_offset(100)
        self.assertIsNotNone(attachm.attachment_b)

    def test_set_attachment_offset_applies_consistent_offset(self):
        attachm = attachment.Attachment(10)
        attachm.set_attachment_vertices()
        attachm.setup_attachment()
        attachm.set_attachment_offset(100)
        core_offset_x = attachm.attachment_b['core_x'] - attachm.attachment_a['core_x']

        attachm_a_vert_x = attachm.attachment_a['vertices'][0]['vert_x']
        attachm_b_vert_x = attachm.attachment_b['vertices'][0]['vert_x']
        vertex_offset_x = attachm_b_vert_x - attachm_a_vert_x

        self.assertEqual(round(core_offset_x, 2), round(vertex_offset_x, 2))

    def test_get_wheel_specs_exists(self):
        self.assertIsNotNone(attachment.Attachment.get_wheel_specs)

    def test_get_wheel_specs_initialises_specs(self):
        attachm = attachment.Attachment(10)
        attachm.get_wheel_specs()
        self.assertIsNotNone(attachm.wheel_specs)

    def test_update_dna_exists(self):
        self.assertIsNotNone(attachment.Attachment.update_dna)

    def test_update_dna_new_dna(self):
        attachm = attachment.Attachment(10)
        new_dna = [[1,2], [3,4], [5,6]]
        attachm.update_dna(new_dna)
        self.assertEqual(attachm.dna, new_dna)

unittest.main()