from single_elevator_sim import *

events = [None, Request(4, -1, 0), Request(2, 1, 3), None, None, None, None, None, None, None, Request(2, 1, 4), Request(0, 1, 2), None, None, None, None, None, None, None, None, None, None, None, None]

ES = Elevator_Simulator(0, 4, events)

for i in range(len(events)): ES.step()

print(ES.get_distance())
