# Class: population
# a contatiner for generated wheel objects, 
# responsible for creating fitness maps and selecting parents for breeding
# ======================

import modules.attachment as attachment
import numpy as np

class Population:
    def __init__(self, pop_size, gene_count):

        # instantiate & store stateful wheel objects
        self.attachments = [attachment.Attachment(gene_count) for i in range(pop_size)]

    # method used to generate the fitness map based on calculated fitnes values
    @staticmethod
    def get_fitness_map(fits):
        fitmap = []
        total = 0
        for fitness in fits:
            total = total + fitness
            fitmap.append(total)
        return fitmap
    
    # method used to select a parent
    # it implements 'roulette wheel selection' using passed fitness map
    @staticmethod
    def select_parent(fitmap, fitness_threshold=0.0):
        # select parent based on fitness and threshold (eg. top 10%, top 50%, etc..)
        r = np.random.uniform(fitness_threshold, 1) #top x%
        r = r * fitmap[-1]
        for i in range(len(fitmap)):
            if r <= fitmap[i]:
                return i

