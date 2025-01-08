class Cart:
    # floor: int
    # direction: int; -1 -> down, 0 -> stationary, 1 -> up
    # distance: int; lifetime floor changes
    def __init__(self, floor = 0):
        self.floor = floor
        self.state = 0
        self.distance = 0
    
    # run every system tick to update floor
    def update_position(self):
        self.floor += self.state
        self.state += abs(self.state)
    
    # change direction
    def update_state(self, dir):
        self.state = dir
    
    # floor getter
    def get_floor(self): return self.floor
    
    # state getter
    def get_state(self): return self.state
    
    # distance getter
    def get_distance(self): return self.distance
    
class Request:
    # c_floor: int; current floor (original request)
    # dir: int; -1 -> down, 1 -> up (original request)
    # t_floor: int; target floor (delayed request)
    def __init__(self, c_floor, dir, t_floor):
        self.c_floor = c_floor
        self.direction = dir
        self.t_floor = t_floor
        
        if not self.verify(): raise Exception("what")
    
    # checks if the request makes sense
    # mostly for sanity once I do fuzz testing
    def verify(self):
        if self.direction == -1: return self.t_floor < self.c_floor
        if self.direction == 1: return self.t_floor > self.c_floor
        return False
    
    # get initial request
    def get_initial_request(self):
        return self.c_floor, self.direction
    
    # reveal target floor only if the elevator is on
    # the current floor
    def get_target_floor(self, elevator):
        if elevator.get_floor() == self.c_floor: return self.t_floor
        else: return None
        
    
