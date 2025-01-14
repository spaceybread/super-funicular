# me when I realise data structures exist
from elevator import *
import heapq as pq

def print_state(elevator, targets, next_targets, missed_dir_requests, current_dir_requests, event=None):
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



targets = set()
next_targets = [] # prio queue for requests in opposite direction
missed_dir_requests = [] # prio queue for requests in the same direction but not at an appropriate floor

current_dir_requests = {} # hash map with request objects

LO, HI = 0, 4
events = [None, Request(4, -1, 0), Request(2, 1, 3), None, None, None, None, None, None, None, Request(2, 1, 4), None, None, None, None, None]
elevator = Cart()

# for now, I'm assuming it takes negligible time to enter/exit a floor within a time step
# I will probaly change this later, implementing two different 'time' mechanisms with real time
# and time step but for now, I don't really want to deal with it

for event in events:
    cur_floor = elevator.get_floor()
    # if the current floor is one of the stops
    if cur_floor in targets:
        # do that stop
        print("stopped at the event above ")
        targets.remove(cur_floor)
        
        # if this stop was part of a request's initial call
        if cur_floor in current_dir_requests:
            reqs = current_dir_requests.get(cur_floor)
            
            if len(targets) == 0:
                elevator.set_state(-1 * elevator.get_state())
            # add all the target floors
            for re in reqs:
                targets.add(re.get_target_floor(elevator))
            
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
    if len(targets) == 0 and len(next_targets) == 0 and len(missed_dir_requests) == 0:
        elevator.set_state(0)
    
    # handle the swapping of sets and hash maps when current set of targets have been cleared
    
    # just move the elevator if it has to be moved when there's no event
    if event == None:
        elevator.update_position()
        print_state(elevator, targets, next_targets, missed_dir_requests, current_dir_requests, event)
        continue
    
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
    
 #   if elevator.get_state() == 1:
 #       if direction == 1:
 #           # matches direction
 #
 #           if floor > cur_floor:
 #               # if it is feasible to stop at that floor, then add it to the targets
 #               targets.add(floor)
 #
 #               if floor in current_dir_requests: current_dir_requests[floor].append(event)
 #               else: current_dir_requests[floor] = [event]
 #
 #           else:
 #               # this is the lowest priority
 #               # prioritise the lowest floors first
 #               pq.heappush(missed_dir_requests, (floor, event))
 #
 #       else:
 #           # prioritise the highest floor first
 #           pq.heappush(next_targets, (-1*floor, event))
 #           # there's not much the elevator can do here except
 #           # queue it for when it switches directions
 #
 #   if elevator.get_state() == -1:
 #       if direction == -1:
 #           # matches direction
 #
 #           if floor < cur_floor:
 #               # if it is feasible to stop at that floor, then add it to the targets
 #               targets.add(floor)
 #
 #               if floor in current_dir_requests: current_dir_requests[floor].append(event)
 #               else: current_dir_requests[floor] = [event]
 #
 #           else:
 #               # this is the lowest priority
 #               # prioritise the lowest floors first
 #               pq.heappush(missed_dir_requests, (-1*floor, event))
 #
 #       else:
 #           # prioritise the highest floor first
 #           pq.heappush(next_targets, (floor, event))
 #           # there's not much the elevator can do here except
 #           # queue it for when it switches directions
    
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
    print_state(elevator, targets, next_targets, missed_dir_requests, current_dir_requests, event)

