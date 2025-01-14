class Cart:
    # floor: int
    # direction: int; -1 -> down, 0 -> stationary, 1 -> up
    # distance: int; lifetime floor changes
    # in_request: boolean; considered in request if the cart has not completed
    #   the second part of the request but has done the first part
    def __init__(self, floor = 0):
        self.floor = floor
        self.state = 0
        self.distance = 0
        self.in_request = False
        self.req = []
    
    # run every system tick to update floor
    def update_position(self):
        self.floor += self.state
        self.distance += abs(self.state)
    
    # add request
    def add_request(self, request):
        self.req.append(request)
        return len(self.req) - 1
    
    # change activity
    def flip_in_request(self): self.in_request = not self.in_request
    
    # change direction
    def set_state(self, dir): self.state = dir
    
    # floor getter
    def get_floor(self): return self.floor
    
    # state getter
    def get_state(self): return self.state
    
    # distance getter
    def get_distance(self): return self.distance
    
    # in_request getter
    def get_request_status(self): return self.in_request
    
    # requests getter
    def get_requests(self): return self.req
    
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
    
    def __lt__(self, other):
        return self.c_floor < other.c_floor
    
    def __eq__(self, other):
        if not isinstance(other, Request): return False
        return self.c_floor == other.c_floor
    
    def __str__(self):
        return f"Request floor: {self.c_floor}, Request direction: {self.direction}, Destination floor: {self.t_floor}"
        
    
