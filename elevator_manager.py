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
            
    def get_best_elevator(self, request):
        c_floor, dir = request.get_initial_request()

        best = 2**32 - 1 # some large value
        idx = -1
        scores = []
        
        for i in range(len(self.elevators)):
            scores.append(compute_score(self.elevators[i], c_floor, dir))
            
            if scores[-1][0] < best:
                best = scores[-1][0]
                idx = i
        
        print(scores) # for debugging
        return idx
        
    
    def compute_score(self, elevator, r_floor, r_dir):
        # logic WIP
        cart = elevator.get_elevator()
        
        if r_dir == cart.get_state():
            if r_dir * cart.get_floor() < r_dir * r_floor:
                return (abs(cart.get_floor() - r_floor), True)
            else:
                # same direction but the request floor has been missed
                pass
        elif r_dir == -1 * cart.get_state():
            # cart is moving in the other direction
            ext = -1
            targets = sorted(lis(televator.targets))
            
            if cart.get_state() == 1: ext = targets[-1]
            else: ext = targets[0]
            
            return (abs(cart.get_floor() - ext) + abs(ext - r_floor), False)
            
            pass
        
        else:
            # cart is currently idle
            return (abs(cart.get_floor() - r_floor), False)
        
