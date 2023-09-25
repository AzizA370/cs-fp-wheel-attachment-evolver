# Class: simulation - stateful
# an environment to assess performance of an individual
# =========================================

# import simulation tools
import modules.sim_tools as sim_tools

# import physics & game engines
import pymunk

class Simulation():

    def __init__(self, sim_id=0):
        self.sim_id = sim_id

    # method to run a wheel individual through the simulation
    def run_wheel(self, attachment, speed=0.0, iterations=2900):
        try:
            run = True
        
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
            sim_tools.SimTools.create_stairs(space, 600, 6000, 800, 60, 90)
            
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
