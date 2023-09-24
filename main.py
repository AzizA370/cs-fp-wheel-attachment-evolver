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
        print('\nLoading evolution cases.\n')
        
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
            
            # CLI RUN MESSAGE
            print('Case: '+case['case_name'],
                    '- initialising population\n')

            # run GA for number of generation
            for gen_num in range(case['gen_num']):

                # Establish sim to run population:
                # run/evaluate each individual in the population through the simulation
                for sim_ind in range(len(pop.attachments)):
                    attachm = pop.attachments[sim_ind]
                    # instantiate a new simulation
                    sim = simulation.Simulation()

                    # CLI RUN MESSAGE
                    print('Case: '+case['case_name'],
                    '- evaluating Indiv# '+str(sim_ind) +'/'+str(len(pop.attachments)-1)
                    +' - '+'Gen# '+str(gen_num)+'/'+str(case['gen_num']-1))

                    # run vehicle individual through simulation
                    sim.run_wheel(attachm, speed=2.0, iterations=2900)

                # get fitness scores of vehicles
                fits = [attachm.get_dist_travelled() 
                        for attachm in pop.attachments]

                # # identify best performer (elite individual)
                # max_fit = np.max(fits)
                # for attachm in pop.attachments:
                #     if attachm.get_dist_travelled() == max_fit:
                #         elite_dna = attachm.dna
                #         break

                # number of vertices per individual
                attachms_vert_num = [len(attachm.dna) 
                                        for attachm in pop.attachments]

                # new list to store new generation of vehicles
                new_attachmens = []

                # create the fitness map - used to dictate bred parents via roulette wheel selection
                fit_map = population.Population.get_fitness_map(fits)
                
                # CLI RUN MESSAGE
                print('\nCase: '+case['case_name'], 
                '- applying crossover & mutation to population individuals')

                # select 2 parents for each vehicle in the evaluated population and breed them
                for i in range(len(pop.attachments)):
                    
                    # Crossover & Mutation:
                    # select first parent
                    parent_a_index = population.Population.select_parent(fit_map)
                    # select second parent
                    parent_b_index = population.Population.select_parent(fit_map)
                
                    # store parents
                    parent_a = pop.attachments[parent_a_index]
                    parent_b = pop.attachments[parent_b_index]

                    # perfrom dna crossover - uniform gene selection
                    # >>>> MAKE IT ACCOUNT FOR FITNESS OF EACH PARENT (BIAS GENE SELECTION)
                    new_dna = genome.Genome.uniform_crossover(parent_a.dna, parent_b.dna)

                    # >> Mutations
                    # perfrom dna point mutate
                    new_dna = genome.Genome.point_mutate(new_dna, rate=case['mute_rate'], amount=case['mute_amount'])
                    # perfrom dna shrink mutate
                    new_dna = genome.Genome.shrink_mutate(new_dna, rate=case['mute_rate'])
                    # perfrom dna grow mutate
                    new_dna = genome.Genome.grow_mutate(new_dna, rate=case['mute_rate'])
                    # perfrom dna swap mutate
                    new_dna = genome.Genome.swap_mutate(new_dna, rate=case['mute_rate'])
                    # perfrom dna scramble mutate
                    new_dna = genome.Genome.scramble_mutate(new_dna, rate=case['mute_rate'], subset_ratio=case['mute_subset'])
                    # perfrom dna scramble mutate
                    new_dna = genome.Genome.invert_mutate(new_dna, rate=case['mute_rate'], subset_ratio=case['mute_subset'])

                    # prepare new generation:
                    # instantaie a new attachment object
                    new_attachment = attachment.Attachment(1)
                    # set its dna to be the bred/mutated dna
                    new_attachment.update_dna(new_dna)
                    # add attachment to new_attachments list
                    new_attachmens.append(new_attachment)

                # CLI RUN MESSAGE
                print('Case: '+case['case_name'], '- setting elites of next generation')

                # elitism - identify and keep best performer in the popultion
                max_fit = np.max(fits)
                for attachm in pop.attachments:
                    if attachm.get_dist_travelled() == max_fit:
                        elite_dna = attachm.dna
                        # instantaie a new vehicle object
                        new_attachment = attachment.Attachment(1)
                        # set its dna to be the bred/mutated dna
                        new_attachment.update_dna(elite_dna)
                        # add vehicle to new_vehicles list
                        new_attachmens[0] = new_attachment
                        break
                
                # store run data in the analyser per generation
                anl.store_gen_data(fits, attachms_vert_num, elite_dna)


                # CLI RUN MESSAGE
                print('Case: '+case['case_name'], 
                '- updating population with next generation indviduals.\n')

                # update population with new generation of vehicles
                pop.attachments = new_attachmens
            
            # CLI RUN MESSAGE
            print('Case: '+case['case_name'], 
            '- generating case analytics..\n')

            # generate case stats & analytics
            anl.process_case_data(case['case_name'])

            # CLI RUN MESSAGE
            print('Case: '+case['case_name'], 
            '- Evolution and Anlysis Complete.\n')

if __name__ == "__main__":
         main()