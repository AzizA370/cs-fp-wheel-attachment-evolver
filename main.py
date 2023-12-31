# Module: main - Entry point of the application
# used to import and implement all GA's components
# ===================

# import all relevant GA modules 
# import modules.genome as genome
import modules.genome as genome
import modules.attachment as attachment
import modules.population as population
import modules.simulation as simulation
import modules.analyser as analyser

# import other helpful modules
import numpy as np
import sys
import os

def main():

        # instantiate an analyser object
        anl = analyser.Analyser()

        # CLI RUN MESSAGE
        print('Importing GA evolution cases.\n')
        
        # get evolution cases from JSON file to setup ga run cases
        anl.load_cases_from_json('ga_cases.json')

        # run GA for each preset case
        for case in anl.ga_run_cases:
            
            # CLI RUN MESSAGE
            print('\nCase: '+case['case_name'],
                    '- loading case specification\n')

            # establish a population based on case specs,
            # instantiates & contains stateful vehicle objects
            pop = population.Population(case['pop_size'], gene_count=case['gene_count'])

            # instantaie a threaded sim object
            sim = simulation.ThreadedSim(pool_size=12)
            
            # CLI RUN MESSAGE
            print('Case: '+case['case_name'],
                    '- initialising population\n')

            # run GA for number of generation
            for gen_num in range(case['gen_num']):

                # CLI RUN MESSAGE
                print('Case: '+case['case_name'],'- evaluating Gen# '+str(gen_num+1)+'/'+str(case['gen_num']))

                # evaluate the population using the sim
                sim.eval_population(pop, 1.0, 2400)

                # get fitness scores of vehicles
                fits = [attachm.get_dist_travelled() 
                        for attachm in pop.attachments]

                # number of vertices per individual
                attachms_vert_num = [len(attachm.dna) 
                                        for attachm in pop.attachments]

                # new list to store new generation of vehicles
                new_attachmens = []

                # create the fitness map - used to dictate bred parents via roulette wheel selection
                fit_map = population.Population.get_fitness_map(fits)
                
                # select 2 parents for each vehicle in the evaluated population and breed them
                for i in range(len(pop.attachments)):
                    
                    # Crossover & Mutation:
                    # select first parent
                    parent_a_index = population.Population.select_parent(fit_map, case['fitt_limit'])
                    # select second parent
                    parent_b_index = population.Population.select_parent(fit_map, case['fitt_limit'])
                
                    # store parents
                    parent_a = pop.attachments[parent_a_index]
                    parent_b = pop.attachments[parent_b_index]

                    # store fitness of each parent
                    parent_a_fitness = parent_a.get_dist_travelled()
                    parent_b_fitness = parent_b.get_dist_travelled()

                    # perfrom dna crossover - weighted uniform gene selection
                    new_dna = genome.Genome.uniform_crossover(parent_a.dna, parent_b.dna,
                                                                parent_a_fitness, parent_a_fitness)

                    # >> Mutations
                    # perfrom dna mutatation (point, shrink, grow, swap, scamble inversion),
                    # rate and amount are set based on given GA case
                    new_dna = genome.Genome.apply_mutations(new_dna, case['mute_rate'], 
                                                            case['mute_amount'],
                                                            case['mute_subset'])

                    # prepare new generation:
                    # instantaie a new attachment object
                    new_attachment = attachment.Attachment(1)
                    # set its dna to be the bred/mutated dna
                    new_attachment.update_dna(new_dna)
                    # add attachment to new_attachments list
                    new_attachmens.append(new_attachment)

                # CLI RUN MESSAGE
                print('Case: '+case['case_name'], '- Setting elite of next generation')

                # elitism - identify and keep best performer in the popultion
                max_fit = np.max(fits)
                for attachm in pop.attachments:
                    if attachm.get_dist_travelled() == max_fit:
                        # store elite's dna
                        elite_dna = attachm.dna
                        # # instantaie a new vehicle object
                        new_attachment = attachment.Attachment(1)
                        # set its dna to be the elite's dna
                        new_attachment.update_dna(elite_dna)
                        # add vehicle to new_vehicles list
                        new_attachmens[0] = new_attachment
                        break
                
                # store run data in the analyser per generation
                anl.store_gen_data(fits, attachms_vert_num, elite_dna)


                # CLI RUN MESSAGE
                print('Case: '+case['case_name'],'- Updating population.\n')

                # update population with new generation of vehicles
                pop.attachments = new_attachmens
            
            # generate case stats & analytics
            anl.process_case_data(case['case_name'])

            # CLI RUN MESSAGE
            print('Case: '+case['case_name'], 
            '- Evolution and Anlysis Complete.\n')

if __name__ == "__main__":
         main()