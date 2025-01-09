# sanity check program to see if the Cart and Request classes work as intended
# I'm going to base it on Donald Knuth's elevator thing from AoCP

from elevator import *

lowest, highest = 0, 4
# events = [None, Request(2, 1, 4), None, Request(3, 1, 4), None, None, Request(4, -1, 0)]
events = [None, Request(2, 1, 4), None, None, None, None, None]
elevator = Cart()

# think of events as any command issued to the elevator from outside the elevator
# a None event just means that for that time tick, there was no command issued
# an assumption that I'm using here is that it takes one time step to enter/exit
# an elevator cart, this is not entirely realistic but I'm running with it for now

TARGET = None
LOG = []

for event in events:
    print("Floor:", elevator.get_floor(), "State:", elevator.get_state())
    if event == None:
        # empty time step, move if required
        if elevator.get_floor() == TARGET: elevator.update_state(0)
        elevator.update_position()
        continue
    
    if elevator.get_state() == 0:
        # cart is unassigned and can be assinged this event
        floor, dir = event.get_initial_request()
        ele_floor = elevator.get_floor()
        elevator.flip_in_request()
        
        if floor == ele_floor:
            # if the cart is already at the floor
            elevator.update_state(dir)
            TARGET = event.get_target_floor(elevator)
            # don't update the position,
            continue
        
        else:
            # if the cart is somewhere else, move to that position
            elevator.update_state((floor - ele_floor) // abs(floor - ele_floor))
            TARGET = floor
            elevator.update_position()
            continue
    
    

print(elevator.get_distance())
