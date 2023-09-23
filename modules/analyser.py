# Class: Analyser
# Responsible for anlysing preformance and GA data as it runs
# stores relevant data produces plots and reports about the performance of the GA
# ======================

import modules.attachment as attachment
import numpy as np
import csv

'''
analyser behaviour:

stateful object

sets system run cases/specs (rounds, GA varaibles, etc..)

per run case:
    as GA runs:
        > COLLECT and store relavent data (per gen)
            - fitness stats (max, mean dist)
            - indvidual stats (mean verts num & dist)
            - elite dna (per%num?) (for drawing, accessing later etc..)
    after GA runs a case:
        > PROCESS stored data
        > GENERATE reports
        > CLEAR stored data
    Got to next case
'''

class Analyser:
    def __init__(self):

        # property which sets evolution specs per GA run,
        # used to set GA run variables
        self.ga_run_cases = [
            {
            'case_name':'all_low',
            'gen_num': 2,
            'pop_size': 2,
            'gene_count': 7,
            'mute_rate': 0.3,
            'mute_amount': 0.05,
            'mute_subset': 0.25,
            'fitness_limit': 0.8,
            }
            ]
        
        # property to store generational data as the GA runs a case
        self.case_run_data = []

    # method used to store evolution data per generation,
    def store_gen_data(self, fitness, vertices_num):
        
        # calculate and store relevant generation stats:
        # calculate mean distance
        mean_dist = np.round(np.mean(fitness), 3)

        # calculate generational change in mean distance
        #if first generation
        mean_dist_change = 0
        if(len(self.case_run_data) != 0):
            # compute change in mean distance from last generation
            mean_dist_change = np.round(mean_dist - self.case_run_data[-1]['mean_dist'], 2)

        # construct generation data instance and add other stats
        gen_run_data = {
            'gen_num': len(self.case_run_data),
            'min_dist': np.round(np.min(fitness), 2),
            'max_dist': np.round(np.max(fitness), 2),
            'mean_dist': mean_dist,
            'mean_dist_change': mean_dist_change,
            'mean_verts': np.round(np.mean(vertices_num))
            # 'elite_dna': elite_dna
        }

        # append generation data
        self.case_run_data.append(gen_run_data)

    def process_case_data(self, case_name):

        # setup outputfolder/subfolders
        """ root > cases_analysis 
                    > [case_name, ..., case_name]
                        elites csv folder, case plot(s), case_csv
         """

        # populate diff case analytics:
        
        # generate case summary csv file
        self.create_case_csv('cases_analytics/'+case_name)
        # case plot
        # wheel drawing

    # method used to accses stored case and generate a csv summary file of the case run
    def create_case_csv(self, file_path):

        # set file name
        file_name = file_path + '.csv'

        # open the file in write mode
        with open(file_path, 'w') as file:

            # instantiate a csv writer
            writer = csv.writer(file)

            # write csv columns for each stored case data key - skip case name
            writer.writerow([colName for colName in self.case_run_data[0].keys()])

            for gen_data in self.case_run_data:
                row = [gen_data['gen_num'], gen_data['min_dist'], gen_data['max_dist'], 
                        gen_data['mean_dist'], gen_data['mean_dist_change'],
                        gen_data['mean_verts']]
                writer.writerow(row)
        