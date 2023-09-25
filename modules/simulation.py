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

            # add the boundries
            sim_tools.SimTools.create_boundries(space, 1500, 800)
            
            # add stairs
            sim_tools.SimTools.create_stairs(space, 600, 10000, 800, 60, 90)
            
            # Introduce individual to physics space:

            # Get wheel specs 
            wheel_specs = attachment.get_wheel_specs(20, 400)

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
# ////
class ThreadedSim():
    def __init__(self, pool_size):
        self.sims = [Simulation(i) for i in range(pool_size)]
    @staticmethod
    def static_run_wheel(sim, attachment, speed=0.0, iterations=2400):
        sim.run_wheel(attachment, speed, iterations)
        return attachment
    def eval_population(self, pop, speed, iterations):
        pool_args = [] 
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.attachments):
            this_pool_args = []
            for i in range(start_ind, start_ind + pool_size):
                if i == len(pop.attachments):
                    break
                sim_ind = i % len(self.sims)
                this_pool_args.append([
                            self.sims[sim_ind], 
                            pop.attachments[i],
                            speed,
                            iterations]   
                )
            pool_args.append(this_pool_args)
            start_ind = start_ind + pool_size
        new_attachmens = []
        for pool_argset in pool_args:
            with Pool(pool_size) as p:
                attachments = p.starmap(ThreadedSim.static_run_wheel, pool_argset)
                new_attachmens.extend(attachments)
        pop.attachments = new_attachmens