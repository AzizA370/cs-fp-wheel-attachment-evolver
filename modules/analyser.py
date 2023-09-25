# Class: Analyser
# Responsible for anlysing preformance and GA data as it runs
# stores relevant data and produces plots and stats
# about the performance of the GA and evolved individuals
# ======================

import json
import modules.attachment as attachment
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import modules.genome as genome
import modules.attachment as attachment

class Analyser:
    def __init__(self):

        # property which sets evolution specs per GA run,
        # recives ga cases specs from loading json file data
        self.ga_run_cases = None

        # property to store generational data as the GA runs a case
        self.case_run_data = []

    # method to handle JSON data and sets GA run cases
    def load_cases_from_json(self, path_to_file):
        
        # accsess the json cases file and load in the cases
        with open(path_to_file) as json_file:
            cases_data = json.load(json_file)

            # store cases in the analyser object
            self.ga_run_cases = cases_data

    # method used to store evolution data per generation,
    def store_gen_data(self, fitness, vertices_num, elite_dna):
        
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
            'mean_verts': np.round(np.mean(vertices_num)),
            'elite_dna': elite_dna
        }

        # append generation data
        self.case_run_data.append(gen_run_data)

    # method used to create a csv stats file of case's evaluated generations
    def process_case_data(self, case_name):

        # elitism > Time tracking > case specs in plot > misc useful info (avg vert dist, etc..)

        # store relative path of cases folder 
        cases__parent_dir = 'cases_analytics/'
        case_folder_path = cases__parent_dir + case_name + '/'

        # create case's folder if it does not exist
        if (not os.path.exists(case_folder_path)):
            os.mkdir(case_folder_path)

        # populate case folder with analytics:

        # 1. generate case stats csv file
        csv_file_name = case_folder_path + 'gens_stats.csv'
        self.create_case_csv(csv_file_name)

        # 2. case plot
        case_plots_dir = case_folder_path + 'plots'
        self.create_case_plots(case_plots_dir, case_name)

        # 3. store elite csvs
        elite_csv_dir = case_folder_path + 'elites_CSVs'
        self.elites_to_csv(elite_csv_dir)

        # 4. draw wheel final elite
        self.draw_best_shape(case_plots_dir, case_name)

        # after performing analys, reset stored case data,
        # in preperatin for next case to be analysed
        self.case_run_data = []

    # method used to accses stored case data and generate a csv summary file of the case run
    def create_case_csv(self, file_path):
        # open the file in write mode
        with open(file_path, 'w') as file:
            # instantiate a csv writer
            writer = csv.writer(file)
            # write csv columns for each stored case data key - skip case name
            writer.writerow([colName for colName in self.case_run_data[0].keys()
                            if colName != 'elite_dna'])

            for gen_data in self.case_run_data:
                row = [gen_data['gen_num'], gen_data['min_dist'], gen_data['max_dist'], 
                        gen_data['mean_dist'], gen_data['mean_dist_change'],
                        gen_data['mean_verts']]
                writer.writerow(row)

    # method used to generate a visual plot using stored case run data
    def create_case_plots(self, file_path, case_name):
        # create case's plots folder if it does not exist
        if (not os.path.exists(file_path)):
            os.mkdir(file_path)
        
        # generate & store case run plots
        # store chart y data
        max_dist = [gen_data['max_dist'] for gen_data in self.case_run_data]
        mean_dist = [gen_data['mean_dist'] for gen_data in self.case_run_data]
        
        # store chart x data
        generations = [gen_data['gen_num'] for gen_data in self.case_run_data]
       
        # calculate trend line
        trend_line_funce = np.polyfit(generations, mean_dist, 1)
        trend = np.poly1d(trend_line_funce)

        # create figure and set its size
        fig, ax = plt.subplots(figsize=(10,7), facecolor=plt.cm.Blues(.2))
        ax.set_facecolor(plt.cm.Blues(0.0))
        
        # set plot title
        header = 'Distance Climbed by Evolved Wheel Attatchment\n'
        sub_header = 'Case: ' + case_name + '*'
        ax.set_title(header + sub_header, fontsize=18, fontweight='bold')

        # plot lines of generational evolution data
        # max distance line
        ax.plot(generations, max_dist, color = plt.cm.Reds(0.3), marker='*', markersize=8)
        # max distance line
        ax.plot(generations, mean_dist, color = plt.cm.cool(0.3), marker='o', markersize=8)
        # mean trend line
        ax.plot(generations, trend(generations), color = plt.cm.cool(0.6), linestyle='dashed')

        # set plot lables
        ax.set_xlabel("Generation Number", fontsize=16)
        ax.set_ylabel("Distance Climbed", fontsize=16)

        # hide right and top borders
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # hide axis tick marks
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticks_position('none')

        # set legends
        ax.legend(['max distance', 'mean distance', 'mean trend'])
        
        # variable to store footer note 
        footer_str = '* Case specs: \n'

        # build up figure footer to note case specs
        for case in self.ga_run_cases:
            if (case['case_name'] == case_name):
                for key in case.keys():
                    if (key == 'case_name'): continue # skip case name
                    footer_str += key+'='
                    footer_str += str(case[key])+' | '
                break

        # set figure footer
        ax.annotate(footer_str,
            xy = (0.5, -0.15),
            xycoords='axes fraction',
            ha='center',
            va="center",
            fontsize=11)

        # set figure layout
        fig.tight_layout()

        # save plot
        plt.savefig(file_path+"/dist_climbed"+".jpg")

        # clear & close the figure, prep for next case
        plt.clf()
        plt.close(1)

    # method to store a csv snapshot of elites' dna structure
    def elites_to_csv(self, file_path):
        # create elites' csv files folder if it does not exist
        if (not os.path.exists(file_path)):
            os.mkdir(file_path)
        
        for gen_data in self.case_run_data:
            # store elite dna per generations
            elite_dna = gen_data['elite_dna']
            
            # name the csv file, indicating gen number
            path_to_file = file_path+'/elite_gen'+str(gen_data['gen_num'])+'.csv'

            # write dna to disk as a csv file usin csv writer defined in the genome module
            genome.Genome.to_csv(elite_dna, path_to_file)

    # method used to draw the shape (morphology) of final elite individual
    def draw_best_shape(self, file_path, case_name):
        
        # get elite dna
        elite_dna = self.case_run_data[-1]['elite_dna']

        # generate graphic of connected vertices around a core
       
        # Get sorted x,y coordinas of elite's vertices:
        # generate genome specs and get x,y cartesian coordinates
        spec = genome.Genome.get_gene_spec()
        genome_discts = genome.Genome.get_genome_dicts(elite_dna, spec)
        elite_coord = attachment.Attachment.set_vertices_coordinates(0, 0, genome_discts)
        
        # sort coordinates by angle size from centre point
        elite_coord = attachment.Attachment.get_clockwise_adjacency(elite_coord)

        # get 1d arrays from the 2d array
        x_values, y_values = np.split(elite_coord,2,axis=1)

        # flatten coordinate x,y component
        x_values = list(x_values.flatten())
        y_values = list(y_values.flatten())

        # duplicate last coordinates pair to get a closed shape
        x_values.append(x_values[0])
        y_values.append(y_values[0])
        
        # create figure and set its size and style
        fig, ax = plt.subplots(figsize=(5,5), facecolor=plt.cm.Blues(.2))
        ax.set_facecolor(plt.cm.Blues(0.0))
        
        # set plot title
        header = 'Evolved Attatchemnt Shape\n'
        sub_header = 'Case: ' + case_name
        ax.set_title(header + sub_header, fontsize=18, fontweight='normal')

        # plot lines of generational evolution data
        # max distance line
        ax.plot(x_values, y_values, color = plt.cm.Blues(0.8), 
                marker='o', markerfacecolor= plt.cm.Oranges(0.3), markersize=7)

        # set plot lables
        ax.set_xlabel("x", fontsize=13)
        ax.set_ylabel("y", fontsize=13)

        dist_travelled = self.case_run_data[-1]['max_dist']
        ver_num = len(elite_dna)
        footer_str = "Distance climbed: " + str(dist_travelled)
        # set figure footer
        ax.annotate(footer_str,
            xy = (0.5, -0.21),
            xycoords='axes fraction',
            ha='center',
            va="center",
            fontsize=12)

        # set figure layout
        fig.tight_layout()
    
        # save plot
        plt.savefig(file_path+"/best_shape"+".jpg")

        # clear & close the figure, prep for next case
        plt.clf()
        plt.close(1)
