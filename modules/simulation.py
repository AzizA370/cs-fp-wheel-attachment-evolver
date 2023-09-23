# Class: simulation - stateful
# an environment to assess performance of an individual
# =========================================
# one Sim One Vehicle ---> Mult. Sims Mult. Vehicles

# import simulation tools
import modules.sim_tools as sim_tools

# import physics & game engines
import pymunk
import pygame

# import pygame utilities
import pymunk.pygame_util

class Simulation():

    def __init__(self):

        # initialuse pygame to use it for visualization
        pygame.init()

        # set preview window width/height
        self.width, self.height = 1500, 800
        
        # initialise the window/surface object
        # self.window = pygame.display.set_mode((self.width, self.height))

    # method to run a wheel individual through the simulation
    def run_wheel(self, attachment, speed=0.0, iterations=2900):
        try:
            run = True
            # clock = pygame.time.Clock()
            
            # set simulation step value - prefered engine value (pymunk docs)
            dt = 0.01

            # set visuls frame per second based on sim steps for consistency
            # fps = 1/dt

            # set up rendering the physics sim (visual render)
            # draw_options = pymunk.pygame_util.DrawOptions(self.window)
            
            # Establish & Setup the simulation environment:
            # setup a pymunk physcis space
            space = pymunk.Space()
            # set sim's gravity
            space.gravity = (0, 981)
            # add the boundries
            sim_tools.SimTools.create_boundries(space, self.width, self.height)
            # add stairs
            sim_tools.SimTools.create_stairs(space, 600, 99999, self.height, 60, 80)
            
            # Introduce individual to physics space
            # Get vehicle specs 
            wheel_specs = attachment.get_wheel_specs(20, 400)

            # Construct the vehicle in the simulation space & set its speed,
            # store its chasis body to track its position
            vehicle_body = sim_tools.SimTools.construct_vehicle(space, wheel_specs, speed)

            # run the simulation for x num of iterations or until manual shutoff
            for step in range(iterations):
                if run is True: # manual shutoff
                
                    # render visuals
                    # self.draw(self.window, space, draw_options)
                    
                    # step the physics sim
                    space.step(dt)

                    # step visual frames
                    # clock.tick(fps)

                    # update vehicle's position as the sim runs
                    attachment.update_position(vehicle_body.position)

                    # shutdown simulation using user events
                    for event in pygame.event.get():
                        # quitting visual simulation protocol
                        if event.type == pygame.QUIT:
                            run = False
                            break
            
            # shutoff the rendere   
            # pygame.quit()
        except:
            print("sim failed to run vehicle, Vertex Count: (Couldn't assign siblings)", len(wheel_specs['attachment_a']['vertices']))

    # method used to draw physical elements and update the pygame visulization screen
    @staticmethod
    def draw(window, space, draw_options):
        
        # draw colored background
        window.fill((50,60,50))

        # draw physics elements on the window
        space.debug_draw(draw_options)

        # refresh the display
        pygame.display.update()