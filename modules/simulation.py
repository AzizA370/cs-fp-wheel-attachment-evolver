# Class: simulation - stateful
# an environment to assess performance of an individual
# =========================================

# import physics & game engines
import pymunk
# import simulation tools
import modules.sim_tools as sim_tools
# import pool from the multi-processing package
from multiprocessing import Pool


class Simulation():

    def __init__(self, sim_id=0):
        # properpty to store simulation id
        self.sim_id = sim_id

    # method to run a wheel individual through the simulation
    def run_wheel(self, attachment, speed=1.0, iterations=2900):
        try:
        
            # set simulation step value - prefered engine value (pymunk docs)
            dt = 0.01
          
            # Establish & Setup the simulation environment:

            # setup a pymunk physcis space
            space = pymunk.Space()

            # set sim's gravity
            space.gravity = (0, 981)

            # add the simulation boundries (walls & floors)
            sim_tools.SimTools.create_boundries(space, 1500, 800)
            
            # add stairs
            sim_tools.SimTools.create_stairs(space, 600, 10000, 800, 60, 90)
            
            # Introduce individual to physics space:

            # Get wheel specs 
            wheel_specs = attachment.get_wheel_specs(20, 300)

            # Construct the vehicle in the simulation space & set its speed,
            # store its chasis body to track its position
            vehicle_body = sim_tools.SimTools.construct_vehicle(space, wheel_specs, speed)

            # run the simulation for x num of iterations
            for step in range(iterations): 
                
                # step the simulation
                space.step(dt)

                # update vehicle's position as the sim runs
                attachment.update_position(vehicle_body.position)

        except:
            print("sim failed to run vehicle, Vertex Count: (Couldn't assign siblings)", len(wheel_specs['attachment_a']['vertices']))

# implmentation of a threaded simulation to utilise parallel computing
# //// Credit:
# This implementation of a threaded simulation was adapted
# from the 'Evolved Creatures' case study showcased in
# the module 'CM_3020 Aritficial Intellegence".
class ThreadedSim():
    def __init__(self, pool_size):
        # instantaie a set number of simulation objects
        self.sims = [Simulation(i) for i in range(pool_size)]

    # create a static copy of the run_wheel method
    @staticmethod
    def static_run_wheel(sim, attachment, speed=1.0, iterations=2400):
        sim.run_wheel(attachment, speed, iterations)
        return attachment

    # evaluate the passes populate for set number of sim iteration/steps
    def eval_population(self, pop, speed, iterations):
        
        # variable to store sim run arguments
        pool_args = [] 
        start_ind = 0
        pool_size = len(self.sims)

        # setup each pool with attachment instances along with run arguments
        while start_ind < len(pop.attachments):
            this_pool_args = []
            # target current pool span
            for i in range(start_ind, start_ind + pool_size):
                if i == len(pop.attachments):
                    break
                sim_ind = i % len(self.sims)
                # store sim arguments
                this_pool_args.append([
                            self.sims[sim_ind], 
                            pop.attachments[i],
                            speed,
                            iterations]   
                )
            pool_args.append(this_pool_args)
            # increment loop index with number equal to number of created sims
            start_ind = start_ind + pool_size
        # new list to store evaluated individuals
        new_attachmens = []
        # run each populated pool and evaluate population indviduals
        for pool_argset in pool_args:
            with Pool(pool_size) as p:
                # perform evaluation and get evaluated attatchment copies
                attachments = p.starmap(ThreadedSim.static_run_wheel, pool_argset)
                # store evaluated attatchments
                new_attachmens.extend(attachments)
        # update population with new attatchments
        pop.attachments = new_attachmens