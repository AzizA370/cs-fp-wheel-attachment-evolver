# Class: Analyser
# Responsible for anlysing preformance and GA data as it runs
# stores relevant data produces plots and reports about the performance of the GA
# ======================

import modules.attachment as attachment
import numpy as np

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

    # method used to store evolution data per generation
    def store_gen_data(self, case_name, fitness, vertices_num):
        # calculate and store relevant generation stats
        gen_run_data = {
            'case_name': case_name,
            'min_dist': np.round(np.min(fitness), 3),
            'max_dist': np.round(np.max(fitness), 3),
            'mean_dist': np.round(np.mean(fitness), 3),
            'mean_verts': np.round(np.mean(vertices_num))
            # 'elite_dna': elite_dna
        }
        # add generation number to run data
        gen_run_data['gen_num'] = len(self.case_run_data)
        # append generation data
        self.case_run_data.append(gen_run_data)