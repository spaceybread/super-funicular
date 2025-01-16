from single_elevator_sim import *
import random

def gen_events_list(LO, HI ):
    events = []

    for i in range(1000):
        if random.randint(0, 31415) % 3 == 0:
            des, dir, tar = -1, -1, -1
            while True:
                des = random.randint(LO, HI)
                dir = random.choice([-1, 1])
                tar = random.randint(LO, HI)
                if (dir == -1 and des > tar) or (dir == 1 and des < tar): break
            
            events.append(Request(des, dir, tar))
        else:
            events.append(None)

    buffer = [None] * int(2.75 * len(events))
    events = events + buffer
    return events

LO, HI = 0, 100
events_1 = gen_events_list(LO, HI)
events_2 = gen_events_list(LO, HI)
events_3 = gen_events_list(LO, HI)

E1 = Elevator_Simulator("E1", LO, HI)
E2 = Elevator_Simulator("E2", LO, HI)
E3 = Elevator_Simulator("E3", LO, HI)

elevators = [E1, E2, E3]

for i in range(len(events_1)):
    E1.add_event(events_1[i])
    E2.add_event(events_2[i])
    E3.add_event(events_3[i])
    
    E1.step()
    E2.step()
    E3.step()

print(E1.get_elevator().get_floor())
print(E2.get_elevator().get_floor())
print(E3.get_elevator().get_floor())
