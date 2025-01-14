from single_elevator_sim import *
import random

# welcome to fuzz testing!

LO, HI = 0, 100
events = []
last = -1

for i in range(1000):
    if random.randint(0, 31415) % 3 == 0:
        des, dir, tar = -1, -1, -1
        while True:
            des = random.randint(LO, HI)
            dir = random.choice([-1, 1])
            tar = random.randint(LO, HI)
            if (dir == -1 and des > tar) or (dir == 1 and des < tar): break
            
        events.append(Request(des, dir, tar))
        last = tar
    else:
        events.append(None)

buffer = [None] * int(2.75 * len(events))
events = events + buffer
ES = Elevator_Simulator("fuzz", LO, HI)



for i in range(len(events)):
    ES.add_event(events[i])
    ES.step()

print("Distance:", ES.get_distance())
print("Final state:", ES.get_elevator().get_state())
print("Worst case:", len(events))
