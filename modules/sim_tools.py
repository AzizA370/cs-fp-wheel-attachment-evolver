# Class: SimTools
# defines and abstracts useful methods to 
# construct pyhsical elements (circles, obticles, wheel/vehicle, etc..)

import pymunk
from pymunk import Vec2d

class SimTools():

    # method to create a physical cricle object and returns it
    @staticmethod
    def create_circle(space, position, radius, mass):
        # create circle body
        circle_body = pymunk.Body()
        # circle_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        
        # get coordinates from position tuple
        x, y = position
        pos_vector = Vec2d(x, y)

        # set circle position
        circle_body.position = pos_vector

        # set circle shape and physcial properties
        circle_shape = pymunk.Circle(circle_body, radius)
        circle_shape.color = (230, 230, 180, 100)
        circle_shape.mass = mass
        circle_shape.filter = pymunk.ShapeFilter(group=10)
        
        # add the circle to the space
        space.add(circle_body, circle_shape)

        # return the circle body object
        return circle_body
    
    @staticmethod
    # method to connect two physical vertices using a segment and joints
    def connect_vert_to_vert(space, vert1_body, vert2_body, segment_mass, segment_thickness):

        # create a new segment and add it to the space
        segment_body = pymunk.Body()
        # segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, vert2_body.position, vert1_body.position, segment_thickness)
        segment_shape.mass = segment_mass
        segment_shape.color = (20, 80, 250, 100)
        segment_shape.filter = pymunk.ShapeFilter(group=10)
        segment_shape.friction = 1
        # segment_shape.elasticity = 1
        space.add(segment_body, segment_shape)

        # create a joint between the segment and first vertex
        seg_vert1_joint = pymunk.PivotJoint(segment_body, vert1_body, vert1_body.position)
        # disable joint collisions
        seg_vert1_joint.collide_bodies = False
        # add joint to space
        space.add(seg_vert1_joint)

        # lock joint's rotation
        seg_vert1_lock = pymunk.RotaryLimitJoint(segment_body, vert1_body, 0, 0)
        # disable joint collisions
        seg_vert1_lock.collide_bodies = False
        # add joint to space
        space.add(seg_vert1_lock)

        # create a joint between the segment and second vertex
        seg_vert2_joint = pymunk.PivotJoint(segment_body, vert2_body, vert2_body.position)
        # disable joint collisions
        seg_vert2_joint.collide_bodies = False
        # add joint to space
        space.add(seg_vert2_joint)

        # lock joint's rotation
        seg_vert2_lock = pymunk.RotaryLimitJoint(segment_body, vert2_body, 0, 0)
        # disable joint collisions
        seg_vert2_lock.collide_bodies = False
        # add joint to space
        space.add(seg_vert2_lock)
    
    # method to create a poly shape and connects both wheels/attatchment to it
    @staticmethod
    def build_chasis(space, core_body_a, core_body_b):

        # set chasis coordinate to be in between both wheel
        pos_x = (core_body_a.position.x + core_body_b.position.x)/2
        pos_y = core_body_a.position.y

        # create chasis body at calculated position
        chas_body = pymunk.Body()
        # chas_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        chas_body.position = (pos_x, pos_y)

        # set contact position between each wheel and the chasis
        wheel_a_contact = core_body_a.position - chas_body.position
        wheel_b_contact = core_body_b.position - chas_body.position
        
        # set poly's vertices
        chasis_verts = [wheel_b_contact, wheel_a_contact, (0, -60)]

        # set poly shape & physical properties
        chas_shape = pymunk.Poly(chas_body, chasis_verts, radius=2)
        chas_shape.color = (115, 120, 250, 100)
        chas_shape.mass = 10000000
        # chas_shape.density = 0.01
        # chas_shape.elasticity = 0.5
        # chas_shape.friction = 0.5

        # nullify chasis collison with wheels
        chas_shape.filter = pymunk.ShapeFilter(group=10)

        # add chasis to the physics space
        space.add(chas_body, chas_shape)

        # attach chasis to first wheel
        chasis_wheel_a_joint = pymunk.PinJoint(chas_body, core_body_a, wheel_a_contact, (0,0))
        chasis_wheel_a_joint.collide_bodies = False
        space.add(chasis_wheel_a_joint)

        # attach chasis to first wheel
        chasis_wheel_b_joint = pymunk.PinJoint(chas_body, core_body_b, wheel_b_contact, (0,0))
        chasis_wheel_b_joint.collide_bodies = False
        space.add(chasis_wheel_b_joint)

        # return chasis body
        return chas_body
    
    # method to create and attach motors to wheels
    # returns the motors for later controls
    @staticmethod
    def set_motors(space, chasis_body, core_body_a, core_body_b, speed):

        # create simple motors between chasis and both wheels
        motor_a = pymunk.SimpleMotor(chasis_body, core_body_a, -speed)
        motor_a.collide_bodies = False
        
        motor_b = pymunk.SimpleMotor(chasis_body, core_body_b, -speed)
        motor_b.collide_bodies = False

        
        # add motors to space
        space.add(motor_a)
        space.add(motor_b)

    # method used to construct and add completely built vehicle to a physics space
    # uses passed wheel specs and other static methods to produce a sim-ready vehicle
    # returns its chasis body object for positional tracking
    @staticmethod
    def construct_vehicle(space, wheel_specs, speed):
        
        # store relevant wheel specs
        core_radius = wheel_specs['core_radius']
        attachment_a = wheel_specs['attachment_a']
        attachment_b = wheel_specs['attachment_b']

        # add wheel cores to the space and store core bodies for vert-core connection
        core_a_body = SimTools.create_circle(space, (attachment_a['core_x'], attachment_a['core_y']), core_radius, 10000000)
        core_b_body = SimTools.create_circle(space, (attachment_b['core_x'], attachment_b['core_y']), core_radius, 10000000)

        # declare empty lists which store vertex bodies for vert-vert connections
        attachment_a_vert_bodies = []
        attachment_b_vert_bodies = []

        # create bodies for wheel vertices, store them, and add them to the physics space
        for i in range(len(attachment_a['vertices'])):

            # get attachment_a vertex coordinates
            vert_a_x = attachment_a['vertices'][i]['vert_x']
            vert_a_y = attachment_a['vertices'][i]['vert_y']
            
            # get attachment_b vertex coordinates
            vert_b_x = attachment_b['vertices'][i]['vert_x']
            vert_b_y = attachment_b['vertices'][i]['vert_y']

            # add attachment_a vertex to the space and store its body object
            attachment_a_vert_body = SimTools.create_circle(space, (vert_a_x, vert_a_y), 1, 100000)

            # add attachment_b vertex to the space and store its body object
            attachment_b_vert_body = SimTools.create_circle(space, (vert_b_x, vert_b_y), 1, 100000)

            # store attachment's vertex body object
            attachment_a_vert_bodies.append(attachment_a_vert_body)
            attachment_b_vert_bodies.append(attachment_b_vert_body)
        
        # after vertex body objects had been initialised, connect vertices and core bodies 
        for i in range(len(attachment_a_vert_bodies)):
            
            # Vert-Core Connections

            # get attachment_a, attachment_b vertex bodies
            attachment_a_vert_body = attachment_a_vert_bodies[i]
           
            attachment_b_vert_body = attachment_b_vert_bodies[i]

            # connect each vertex from attachment_a to its core
            SimTools.connect_vert_to_vert(space, core_a_body, attachment_a_vert_body, 100000, 2)
            
            # connect each vertex from attachment_b to its core
            SimTools.connect_vert_to_vert(space, core_b_body, attachment_b_vert_body, 100000, 2)

            # Vert-Sibling_Vert Connections

            # store indices of vert's siblings - attachment_a
            attachment_a_vert_sibling_a_index = attachment_a['vertices'][i]['sibling_a']
            attachment_a_vert_sibling_b_index = attachment_a['vertices'][i]['sibling_b']
            
            # store indices of vert's siblings - attachment_b
            attachment_b_vert_sibling_a_index = attachment_b['vertices'][i]['sibling_a']
            attachment_b_vert_sibling_b_index = attachment_b['vertices'][i]['sibling_b']

            # get vertices'es sibling bodies from vertex body list using their stored indices - attachment_a
            attachment_a_vert_sibling_a_body = attachment_a_vert_bodies[attachment_a_vert_sibling_a_index]
            attachment_a_vert_sibling_b_body = attachment_a_vert_bodies[attachment_a_vert_sibling_b_index]

            # get vertices'es sibling bodies from vertex body list using their stored indices - attachment_b
            attachment_b_vert_sibling_a_body = attachment_b_vert_bodies[attachment_b_vert_sibling_a_index]
            attachment_b_vert_sibling_b_body = attachment_b_vert_bodies[attachment_b_vert_sibling_b_index]

            # connect each vertex in attachment_a to its 2 sibling vertices
            SimTools.connect_vert_to_vert(space, attachment_a_vert_body, attachment_a_vert_sibling_a_body, 100000, 2)
            SimTools.connect_vert_to_vert(space, attachment_a_vert_body, attachment_a_vert_sibling_b_body, 100000, 2)
            
            # connect each vertex in attachment b to its 2 sibling vertices
            SimTools.connect_vert_to_vert(space, attachment_b_vert_body, attachment_b_vert_sibling_a_body, 100000, 2)
            SimTools.connect_vert_to_vert(space, attachment_b_vert_body, attachment_b_vert_sibling_b_body, 100000, 2)

        # create and add vehicle's chasis to the physics space
        chasis_body = SimTools.build_chasis(space, core_a_body, core_b_body)

        # create and attach wheel motors
        SimTools.set_motors(space, chasis_body, core_a_body, core_b_body, speed)

        # return chasis body to track vehicle's position
        return chasis_body
            
    # method used to construct stair bodies in the simulation
    @staticmethod
    def create_stairs(space, from_x, to_x, height, stair_width, stair_height_inc):

        # calculate number of stairs
        stairs_num = int((to_x - from_x) / stair_width)

        # create a body for each stair unit
        for num in range(stairs_num):
            stair_body = pymunk.Body(body_type=pymunk.Body.STATIC)

            # calculate x position
            stair_x = from_x + (num * stair_width)

            # set position
            stair_body.position = (stair_x, height)

            stair_shape = pymunk.Poly.create_box(stair_body, (stair_width, stair_height_inc * num), 1)
            stair_shape.filter = pymunk.ShapeFilter(group=1) # nullify stairs-boundry collisions
            stair_shape.friction = 0.6
            stair_shape.color = (250, 250, 40, 100)
            space.add(stair_body, stair_shape)
    
    # method used to set walls around the simulation space
    @staticmethod
    def create_boundries(space, width, height):
        
        # specify boundry coordinates
        boundry_coords = [
            [(0, 0), (0, height)], # left wall
            [(0, height), (width * 10, height)], # bottom floor
        ]

        # draw boundries at sepecified dimensions
        for x, y in boundry_coords:
            
            # create body/shapes
            boundry_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            boundry_shape = pymunk.Segment(boundry_body, x, y, 10)
            
            # specify shape attributes
            boundry_shape.color = (150, 150, 190, 100)
            boundry_shape.friction = 1
            boundry_shape.filter = pymunk.ShapeFilter(group=1) # nullify stairs-boundry collision
            
            # add body/shape to space
            space.add(boundry_body, boundry_shape)