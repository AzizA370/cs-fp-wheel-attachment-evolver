# Module: main - Entry point of the application
# used to importt and implement all GA's components
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
        # store preset ga run cases
        run_cases = anl.ga_run_cases

        # run GA for each preset case
        for case in run_cases:
            # establish a population based on case specs,
            # instantiates & contains stateful vehicle objects
            pop = population.Population(case['pop_size'], gene_count=case['gene_count'])

            # run GA for number of generation
            for gen in range(case['gen_num']):

                # Establish sim to run population:
                # run/evaluate each individual in the population through the simulation
                for attachm in pop.attachments:

                    # instantiate a new simulation
                    sim = simulation.Simulation()

                    # run vehicle individual through simulation
                    sim.run_wheel(attachm, speed=1.5, iterations=500)

                # get fitness scores of vehicles
                fits = [attachm.get_dist_travelled() 
                        for attachm in pop.attachments]
                print('Gen'+str(gen)+':', fits, 'Avg Fitness:', np.mean(fits),'\n')

                attachms_vert_num = [len(attachm.dna) 
                                        for attachm in pop.attachments]
                print('attachment vertices num', attachms_vert_num)

                # store run data in the analyser
                anl.store_gen_data(case['case_name'], fits, attachms_vert_num)
                print(anl.case_run_data)
                # new list to store new generation of vehicles
                new_attachmens = []

                # create the fitness map - used to dictate bred parents via roulette wheel selection
                fit_map = population.Population.get_fitness_map(fits)
                
                # >> Breeding
                # select 2 parents for each vehicle in the evaluated population and breed them
                for i in range(len(pop.attachments)):
                    # //////////Breeding & Mutation
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

                # elitism- keep best in generation in population and in .csv
                max_fit = np.max(fits)
                for attachm in pop.attachments:
                    if attachm.get_dist_travelled() == max_fit:
                        # instantaie a new vehicle object
                        new_attachment = attachment.Attachment(1)
                        # set its dna to be the bred/mutated dna
                        new_attachment.update_dna(attachm.dna)
                        # add vehicle to new_vehicles list
                        new_attachmens[0] = new_attachment
                        # export elite's dna construct to local storage
                        file_name = 'elites-dna-csv/elite_Gen'+str(gen)+'.csv'
                        genome.Genome.to_csv(attachm.dna, file_name)
                        break
                
                # update population with new generation of vehicles
                pop.attachments = new_attachmens
            
            # generate case stats & analytics
            # anl.
            print('END of CASE, Genrating Stats..')

if __name__ == "__main__":
         main()