from elevator import *
import heapq as pq

class Elevator_Simulator:
    def __init__(self, name, LO, HI, events = None, debug = False):
        self.LO, self.HI = LO, HI
        self.elevator = Cart()
        
        self.name = name
        self.debug = debug
        self.targets = set()
        self.next_targets = [] # prio queue for requests in opposite direction
        self.missed_dir_requests = [] # prio queue for requests in the same direction but not at an appropriate floor
        self.current_dir_requests = {} # hash map with request objects
        
        self.events = events if events is not None else []
        self.event_idx = 0
    
    def add_event(self, event = None): self.events.append(event)
    
    def step(self):
                self.elevator, self.targets, self.next_targets, self.missed_dir_requests, self.current_dir_requests = self.step_func(self.elevator, self.targets, self.next_targets, self.missed_dir_requests, self.current_dir_requests)
    
    def step_func(self, elevator, targets, next_targets, missed_dir_requests, current_dir_requests):
        event = self.events[self.event_idx]
        self.event_idx += 1
        
        cur_floor = elevator.get_floor()
        
        if elevator.get_state() == -1:
            if sorted(list(targets))[0] >= cur_floor:
                elevator.set_state(1)
        elif elevator.get_state() == 1:
            if sorted(list(targets))[-1] <= cur_floor:
                elevator.set_state(-1)
        
        # if the current floor is one of the stops
        if cur_floor in targets:
            # do that stop
            targets.remove(cur_floor)
        
            # if this stop was part of a request's initial call
            if cur_floor in current_dir_requests:
                reqs = current_dir_requests.get(cur_floor)
            
                # add all the target floors
                for re in reqs:
                    targets.add(re.get_target_floor(elevator))
            
                if len(targets) == 0:
                    elevator.set_state(-1 * elevator.get_state())
            
                current_dir_requests[cur_floor] = []
    
            if len(targets) == 0:
                # time for a switch
                if len(next_targets) > 0:
                    current_dir_requests.clear()
                    highest = next_targets[0][1]
            
                    while next_targets:
                        _, req = pq.heappop(next_targets)
                        f, d = req.get_initial_request()
                        if f != cur_floor:
                            targets.add(f)
                            # this bug fix took days
                            if f in current_dir_requests: current_dir_requests[f].append(req)
                            else: current_dir_requests[f] = [req]
                        else:
                            targets.add(req.get_target_floor(elevator))
                        
                    next_targets = missed_dir_requests
                    missed_dir_requests = []
            
                    hf, df = highest.get_initial_request()
                    elevator.set_state((hf - cur_floor) // abs(hf - cur_floor) if abs(hf - cur_floor) != 0 else df)
        
                else:
                    if len(missed_dir_requests) > 0:
                        _, req = missed_dir_requests[0]
                        f, d = req.get_initial_request()
                        targets.add(f)
                        next_targets = missed_dir_requests
                        missed_dir_requests = []
                        elevator.set_state(-1 * elevator.get_state())
                        current_dir_requests.clear()
                    else:
                        elevator.set_state(0)
            
    
        # if targets have been cleared and there are no more requests, relax
        if len(targets) == 0 and len(next_targets) == 0 and len(missed_dir_requests) == 0: elevator.set_state(0)
    
        # handle the swapping of sets and hash maps when current set of targets have been cleared
    
        # just move the elevator if it has to be moved when there's no event
        if event == None:
            elevator.update_position()
            if self.debug: self.print_state(elevator, targets, next_targets, missed_dir_requests, current_dir_requests, event)
            return elevator, targets, next_targets, missed_dir_requests, current_dir_requests
    
        floor, direction = event.get_initial_request()
    
        # if the elevator is currently unassigned, assign it
        if elevator.get_state() == 0:
            targets.add(floor)
            elevator.set_state((floor - cur_floor) // abs(floor - cur_floor) if abs(floor - cur_floor) != 0 else direction)
        
            if direction == elevator.get_state():
                if floor in current_dir_requests: current_dir_requests[floor].append(event)
                else: current_dir_requests[floor] = [event]
            else:
                pq.heappush(next_targets, (-1 * direction * floor, event))
        
        # manage queuing
        elif elevator.get_state() == direction:
            if direction * floor > direction * cur_floor:
                targets.add(floor)
                if floor in current_dir_requests: current_dir_requests[floor].append(event)
                else: current_dir_requests[floor] = [event]
            else:
                pq.heappush(missed_dir_requests, (direction * floor, event))
        else:
            pq.heappush(next_targets, (-1 * direction * floor, event))
        
        # handle requests that are made when the elevator is moving for each direction
        # if they're in the same direction as current motion and and can be picked up, then pick up
        # if they're in the other direction put it in the next prio queue
        # if they're in the same direction as current moition but cannot be picked up, then put it in the last prio queue
    
        elevator.update_position()
        if self.debug: self.print_state(elevator, targets, next_targets, missed_dir_requests, current_dir_requests, event)
        return elevator, targets, next_targets, missed_dir_requests, current_dir_requests
    
    def print_state(self, elevator, targets, next_targets, missed_dir_requests, current_dir_requests, event=None):
        event_str = f"Event: {event}" if event else "Event: None"
    
        # elevator details
        cur_floor = elevator.get_floor()
        cur_state = elevator.get_state()
    
        print("\n=== ELEVATOR STATE ===")
        print(f"Floor: {cur_floor} | State: {'Idle' if cur_state == 0 else 'Up' if cur_state == 1 else 'Down'}")
        print(f"Targets: {sorted(targets)}")
        print(f"Next Targets: {[x[1] for x in next_targets]}  # Sorted by priority")
        print(f"Missed Requests: {[x[1] for x in missed_dir_requests]}  # Sorted by priority")
        print(f"Current Direction Requests: {current_dir_requests}")
        print(f"{event_str}")
        print("======================\n")
    
    def get_distance(self):
        return self.elevator.get_distance()
    
    # i dont want to add getters for each of the elevator interface functions
    def get_elevator(self):
        return self.elevator
