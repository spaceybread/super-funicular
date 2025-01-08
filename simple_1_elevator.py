# sanity check program to see if the Cart and Request classes work as intended
# I'm going to base it on Donald Knuth's elevator thing from AoCP

from elevator import *

lowest, highest = 0, 4
events = [None, Request(2, 1, 4), None, Request(3, 1, 4), None, None, Request(4, -1, 0)]
events = [None, Request(2, 1, 4), None, None, None, None, None]
elevator = Cart()

# think of events as any command issued to the elevator from outside the elevator
# a None event just means that for that time tick, there was no command issued

TARGET = None

for event in events:
    if event == None:
        # empty time step, move if required
        if elevator.get_floor() == TARGET: elevator.update_state(0)
        elevator.update_position()
        continue
    
    if elevator.get_state() == 0:
        floor, dir = event.get_initial_request()
        ele_floor = elevator.get_floor()
        
        if floor == ele_floor:
            elevator.update_state(dir)
            TARGET = floor
            continue
