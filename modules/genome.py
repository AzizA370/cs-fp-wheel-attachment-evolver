#Class: genome & spec operations
# ================
import numpy as np
import math
import random
import copy

class Genome():
    
    # method used to generate an array of certain length populated with random floats 0 to 1
    # used to initialise a gene member
    @staticmethod
    def get_random_gene(gene_length):
        gene = np.array([np.random.random() for i in range(gene_length)])
        # gene = np.array([random.uniform(0.7, 1), random.random()])
        return gene

    # a method which generates an array of random 0-1 values
    # array length is determined by number of specs
    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length) for i in range(gene_count)]
        return genome
    
    # method which sets the specifications and scale of genome values - the encoding scheme
    @staticmethod
    def get_gene_spec():
        gene_spec = {

            "vert_dist": {"scale":120},
            "vert_angle": {"scale":360}
        }
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1
        return gene_spec

    # method to generate a dictionary of individual's attributes
    # it scales gene values using both specs and gene array
    @staticmethod
    def get_gene_dict(gene, spec):
        gene_dict = {}
        for key in spec:
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gene_dict[key] = gene[ind] * scale
        return gene_dict

    # method to construct a list of gene dictionaries
    @staticmethod
    def get_genome_dicts(genome, spec):
        genome_dicts = []
        for gene in genome:
            genome_dicts.append(Genome.get_gene_dict(gene, spec))
        return genome_dicts

    # static method used to crossover two dna strands together
    # used to breed two genomes and generated a new genome combination
    # it averages genome size between both parents
    # it selects genes uniformly from either parent (coin filp) to produce the child genome,
    # gene selecttion is biased towards parent with better fitness,
    # where the parent with heigher fitness score contributes more genes 
    @staticmethod
    def uniform_crossover(genome_a, genome_b, genome_a_fitness, genome_b_fitness):
        
        # initialise new genome with average length of genome a & b
        # calcualte avg genome length
        avg_genome_length = math.ceil((len(genome_a) + len(genome_a))/2)

        # create new genome of same type as, and based, on passed genomes
        new_genome = Genome.get_random_genome(len(genome_a[0]), avg_genome_length)

        # calculate selection bias based on parents' fitness (weighted gene selection)
        bias_rate = genome_a_fitness/(genome_a_fitness+genome_b_fitness)

        # perform crossover
        selected_gene = None
        # iterate over each new genome index
        for ind in range(len(new_genome)):
            # select a random gene from either parent
            if random.random() <= bias_rate:
                gene_ind = random.randint(0, len(genome_a)-1)
                selected_gene = genome_a[gene_ind]
            else:
                gene_ind = random.randint(0, len(genome_b)-1)
                selected_gene = genome_b[gene_ind]

            # add selected gene to new genome
            new_genome[ind] = selected_gene

        # return the created child genome
        return new_genome

    # method used to apply point mutation to a genome
    # for a given chance, it alters gene values in a given genome and returns it
    @staticmethod
    def point_mutate(genome, rate, amount):
        # create copy of passed genome
        new_genome = copy.copy(genome)

        # access gene values
        for gene in new_genome:
            for ind in range(len(gene)):
                # check mutation chance
                if random.random() < rate:
                    # generate random alteration factor
                    rand_amount = (random.random() - 0.5) * amount
                    # alter gene value
                    gene[ind] += rand_amount

                # safeguard from illegal gene values (>1.0 & negative floats)
                if gene[ind] >= 1.0:
                    gene[ind] = 0.9999
                if gene[ind] < 0.0:
                    gene[ind] = 0.0
        
        # return the mutated genome
        return new_genome

    # method used to apply shrink mutation to a genome
    # for a given chance, it removes a gene element from a genome and returns it
    @staticmethod
    def shrink_mutate(genome, rate):
        # if genome is at minimum size
        if len(genome) == 1:
            # return the genome as it is
            return copy.copy(genome)
        
        # check mutation chance
        if random.random() < rate:
            # select a random index along the genome
            ind = random.randint(0, len(genome)-1)
            # delete a gene at selected index
            new_genome = np.delete(genome, ind, 0)
            
            # return the mutated genome
            return new_genome
        else:
            # return the genome as it is
            return copy.copy(genome)
    
    # method used to apply grow mutation to a genome
    # for a given chance, it adds a gene element to a genome and returns it
    @staticmethod
    def grow_mutate(genome, rate):
        # check mutation chance
        if random.random() < rate:
            # create a new gene instance with size of other genes
            new_gene = Genome.get_random_gene(len(genome[0]))
            
            # create copy of passed genome
            new_genome = copy.copy(genome)

            # append new gene to the genome
            new_genome = np.append(new_genome, [new_gene], axis=0)
            
            # return the mutated genome
            return new_genome
        else:
            return copy.copy(genome)

    # method used to perform swap mutation on passed genome
    # it selects 2 random genes, and swaps their location in the genome
    @staticmethod
    def swap_mutate(genome, rate):
         # check mutation chance
        if random.random() < rate:
             # create copy of passed genome
            new_genome = copy.copy(genome)

            # select two random index along the genome 
            rand_gene_a_ind = random.randint(0, len(new_genome)-1)
            rand_gene_b_ind = random.randint(0, len(new_genome)-1)
            
            # store copis of corresping gene values
            gene_a = copy.copy(new_genome[rand_gene_a_ind])
            gene_b = copy.copy(new_genome[rand_gene_b_ind])

            # swap values of both genes
            new_genome[rand_gene_a_ind] = gene_b
            new_genome[rand_gene_b_ind] = gene_a
            
            # return the genome
            return new_genome
        else:
            return copy.copy(genome)

    # method used to apply scramble mutation on passed genome
    # it selects a subset of subsequent array elements, 
    # then shuffles their array position before returning a scrambled genome
    # recieves chance of mutation, and genome's ratio to be scrambled
    # (eg. scramble 30% or 50% of genome elements)
    @staticmethod
    def scramble_mutate(genome, rate, subset_ratio):
         # check mutation chance
        if random.random() < rate:
             # create copy of passed genome
            new_genome = copy.copy(genome)

            # calculate size of subset of genome to be scrambled
            subset_size = math.floor(len(genome) * subset_ratio)

            # set scrambling bounds (from/to)
            scramble_from = random.randint(0, len(genome) - subset_size)
            scramble_to = scramble_from + subset_size
            
            # get genome slice which lays within subset bounds
            subset_elements = copy.copy(genome[scramble_from:scramble_to])

            # scramble subset elements
            np.random.shuffle(subset_elements)
            
            # contain shuffled elements in a generic list to enable popping
            scrambled_subset = list(subset_elements)
            
            # set shuffled values at their new location
            for ind in range(scramble_from, scramble_to, 1):
                new_genome[ind] = scrambled_subset.pop(0)
            
            # return scrambled genome
            return new_genome
        else:
            return copy.copy(genome)
    
    # method used to apply inversion mutation on passed genome.
    # it selects a subset of subsequent array elements, 
    # then inverts their array position in the copied genome
    # recieves chance of mutation, and genome's ratio to be inverted
    # (eg. invert 30% or 50% of genome elements)
    @staticmethod
    def invert_mutate(genome, rate, subset_ratio):
         # check mutation chance
        if random.random() < rate:
             # create copy of passed genome
            new_genome = copy.copy(genome)

            # calculate size of subset of genome to be inverted
            subset_size = math.floor(len(genome) * subset_ratio)

            # set inversion bounds (from/to)
            invert_from = random.randint(0, len(genome) - subset_size)
            invert_to = invert_from + subset_size
            
            # get genome slice which lays within subset bounds
            subset_elements = copy.copy(genome[invert_from:invert_to])

            # contain inverted elements in a generic list to enable popping
            inversion_subset = list(subset_elements)
            
            # set inverted values at their new location
            for ind in range(invert_from, invert_to, 1):
                new_genome[ind] = inversion_subset.pop(len(inversion_subset)-1)

            # return inverted genome
            return new_genome
        else:
            return copy.copy(genome)                              

    # method used to export a genome construct to a local .csv file
    @staticmethod
    def to_csv(dna, path_to_file):
        csv_str = ""
        for gene in dna:
            for val in gene:
                csv_str = csv_str + str(val) + ","
            csv_str = csv_str + '\n'

        with open(path_to_file, 'w') as f:
            f.write(csv_str)
    
    # method used to import a genome construct from a local .csv file
    @staticmethod
    def from_csv(path_to_file):
        csv_str = ''
        with open(path_to_file) as f:
            csv_str = f.read()   
        dna = []
        lines = csv_str.split('\n')
        for line in lines:
            vals = line.split(',')
            gene = [float(v) for v in vals if v != '']
            if len(gene) > 0:
                dna.append(gene)
        return dna