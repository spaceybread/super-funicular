from single_elevator_sim import *
from elevator import *

class Elevator_Manager:
    def __init__(self, lo, hi, k = 1):
        self.elevators = []
        self.LO, self.HI = lo, hi
        
        # add k elevators
        for i in range(k): elevators.append(Elevator_Simulator(lo, hi))
    
    def step(self):
        # just step every elevator
        for elevator in self.elevators:
            elevator.step()
            
    def push_request(self, request):
        floors, states = [], []
        c_floor, dir = request.get_initial_request()
        
        # build lists of all states and floors
        for elevator in self.elevators:
            ele = elevator.get_elevator()
            floors.append(ele.get_floor())
            states.append(ele.get_state())
        
        best = 2**32 - 1 # some large value
        idx = -1
        scores = []
        
        for i in range(len(self.elevators)):
            e_floor, e_state = floors[i], states[i]
            scores.append(compute_score(e_floor, e_state, c_floor, dir))
            
            if scores[-1] < best:
                best = scores[-1]
                idx = i
        
        print(scores) # for debugging
        return idx
        
    
    def compute_score(self, e_floor, e_state, r_floor, r_dir):
        # logic WIP
        return 0
