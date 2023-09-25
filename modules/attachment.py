# Attachment Class: 
# generates a stateful representation of the attachment and wheel to be tested
# ============================
import modules.genome as genome
import math
import numpy as np

class Attachment():
    def __init__(self, gene_count):
        # attachment attributes used to set/construct the attachment
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)

        # initial wheel core position
        self.pos_x = 150
        self.pos_y = 600

        # propery to store cartesian coordinates of attachment's vertices 
        self.vertices_pos = None
        
        # properties to store vehicle component's speces
        # property to store main attachment vertices positions,
        # vertix neighbours, and core position
        self.attachment_a = None 
         # property to store duplicte of main attachment with offset applied
        self.attachment_b = None

        # will store final wheel components used to construct it as a vehicle
        self.wheel_specs = None

        # properties to store indvidual's inital/final positions
        self.initial_position = None
        self.final_position = None
    
    # method to set position of vertices around wheel's core based on dna & specs
    # it uses genome's method to convert vertices' from polar coordinates to x,y cartesian coordinates
    # sets the 'vertices_pos' object property
    def set_attachment_vertices(self):
        
        # get genome dictionary
        genom_dicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
        
        # establish and store attachment's vertices' x,y positions around the core
        self.vertices_pos = Attachment.set_vertices_coordinates(self.pos_x, self.pos_y, genom_dicts)

    # method used to setup attachment's position and vertices
    def setup_attachment(self):

        # determine attachment's x,y positions
        attachment_x = self.pos_x
        attachment_y = self.pos_y

        # declare a list - will contain positon and sigblings' index for each attachment vertex
        attachment_vertices = []

        # determine attachment's vertices and their siblings:
        # get clockwise-sorted vertices
        sorted_coordinates = Attachment.get_clockwise_adjacency(self.vertices_pos)
        
        # determine vertex coordinates and its siblings' indices
        for ind in range(len(sorted_coordinates)):
            
            # set vertex'es x,y coordinates
            vert_x = sorted_coordinates[ind][0]
            vert_y = sorted_coordinates[ind][1]

            # determine vertex'es siblings:
            # if first element, set left sibling to be last coordinate index
            if(ind == 0):
                left_sibling_ind = len(sorted_coordinates) - 1
                right_sibling_ind = ind + 1
            # if last element, set right sibling to be first coordinate index (closed shape)
            elif(ind == len(sorted_coordinates)-1):
                left_sibling_ind = ind - 1
                right_sibling_ind = 0
            # otherwise, set lef/right sibling to be adjacent indices
            else:
                left_sibling_ind = ind - 1
                right_sibling_ind = ind + 1

            # create vertex dictionary
            vertex = {
                'vert_x': vert_x,
                'vert_y': vert_y,
                'sibling_a': left_sibling_ind,
                'sibling_b': right_sibling_ind
                }

            # add determined vertex to vertices list
            attachment_vertices.append(vertex)

        # setup the attachment - x,y position, vertices and sbilings per vertex
        self.attachment_a = {
            'core_x': attachment_x,
            'core_y': attachment_y,
            'vertices': attachment_vertices
        }

    # method to construct the second attachment based on the first attachment
    # it applies the horizontal offset to both core and vertices of the
    # second attachment relative to the first
    def set_attachment_offset(self, attachment_offset_x=200):

        # get genome dictionary to access the offset value
        genom_dict = genome.Genome.get_genome_dicts(self.dna, self.spec)

        # store offset value
        x_offset = attachment_offset_x

        # set second attachment to be a copy of the first constructed attachment dictionary
        self.attachment_b = dict(self.attachment_a)
        
        # copy vertices list to second attachment
        self.attachment_b['vertices'] = list(self.attachment_a['vertices'])

        # apply horizontal offset to attachment's core position
        self.attachment_b['core_x'] += x_offset

        # apply horizontal offset to attachment's vertices
        for ind in range(len(self.attachment_b['vertices'])):
            
            # copy each vert object from fist attachment to second attachment
            self.attachment_b['vertices'][ind] = dict(self.attachment_a['vertices'][ind])

            # apply horizontal offset to second attachment's vertices
            self.attachment_b['vertices'][ind]['vert_x'] += x_offset
            
    # method to construct the attachments and returns an object for the simulation to run
    # returned object contains all data required to run and evaluate the attachment morphology by the sim
    def get_wheel_specs(self, core_radius=20, attachment_offset_x=200):

        # setup wheel attributes if they were not initialised prior
        if self.wheel_specs == None:
            
            # initlise specs as an empty dictionary
            self.wheel_specs = {}

            # setup wheel's elements
            self.set_attachment_vertices()
            self.setup_attachment()
            self.set_attachment_offset(attachment_offset_x)

            # combine attributes into a single object
            self.wheel_specs['core_radius'] = core_radius
            self.wheel_specs['attachment_a'] = self.attachment_a
            self.wheel_specs['attachment_b'] = self.attachment_b
        
        # return wheel specs
        return self.wheel_specs

    # method used to calculate x,y coordinates of vertices
    # computes cartesian coordinate from polar coordinate input
    @staticmethod
    def set_vertices_coordinates(core_x, core_y, genome_dicts):
        
        # list to store calculated positions
        verts_pos = []

        # access genome vertex data, distance and angle (polar coordinates)
        for vert in genome_dicts:
            # store vert data - distance & angle
            vert_dist = vert['vert_dist']
            vert_angle = vert['vert_angle']
            
            # convert angle to radians
            vert_angle = vert_angle * math.pi/180.0

            # convert polar coordinates to cartesian coordinates
            pos_x = vert_dist * math.cos(vert_angle)
            pos_y = vert_dist * math.sin(vert_angle)

            # adjust vert coordinates to be relative to core's position
            core_vert_x = core_x + pos_x
            core_vert_y = core_y + pos_y

            # store vertex position as a dictionary
            verts_pos.append([core_vert_x, core_vert_y])
            
        # return position objects list
        return np.array(verts_pos)

    # adapted method used to determine coordinates points' clockwise order around a centre point,
    # such that a closed-shape morphology is determined.
    # it returns sorted list of the passed coodrniate list
    # ///////////
    # Credit:
    # This method 'get_clockwise_adjacency' was adapted from an algorithm I found online.
    # It was presented by 'Pav Creations' on 09th Dec 2022 on their blog post.
    # link to the blog post: 
    # https://pavcreations.com/clockwise-and-counterclockwise-sorting-of-coordinates/
    # ///////////
    @staticmethod
    def get_clockwise_adjacency(coords_list):
        
        # workout point centre of all coordinates
        centre_x, centre_y = coords_list.mean(0)
        
        # transpose the array and get x & y elements saperately
        x, y = coords_list.T
        
        # calculate angle between each point and centre point
        angles = np.arctan2(x - centre_x, y - centre_y)

        # sort indices of coordinates based on angle magnitude from centre point
        # negate angles list for clockwise sorting
        sorted_indices = np.argsort(-angles)

        # return sorted coordinates 
        return coords_list[sorted_indices]

    # create functions to store/update fitness scores as it runs
    def update_position(self, position):
        if self.initial_position == None:
            self.initial_position = position
        else:
            self.final_position = position

    # create function to calculate distance moved
    def get_dist_travelled(self):

        # return 0 if not simulated yet
        if self.initial_position is None or self.final_position is None:
            return 0

        # get positional arguments
        from_x, from_y = self.initial_position
        to_x, to_y = self.final_position

        # calcuate covered distance
        distance_covered = math.dist([from_x, from_y], [to_x, to_y])
        
        return distance_covered

    # method used to update attachment's dna and reset its properties
    def update_dna(self, new_dna):
        
        # set new dna
        self.dna = new_dna
        
        # reset object's properties
        self.vertices_pos = None
        self.attachment_a = None
        self.attachment_b = None
        self.wheel_specs = None
        self.initial_position = None
        self.final_position = None
