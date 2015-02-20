from Node import createMap

__author__ = 'ralphblanes, lmoore44'
import Queue
import Node.py
'''
This is the main simulation class. She'll take an adjacency list and run the simulation based on it.
You can also change the update time through the clock_tick_time parameter(default = 2s)
'''
def simulate(adj_list, clock_tick_time = 2):
    #Adjacency lists are stored in the form Node, {adjacent nodes, edge between them}
    adj_list = createMap("../GTMap.csv")

    #preprocessing step: Allows us to change the distribution of cars in an adjacency list
    change_distribution()

    # We're putting all the requests in here to update them. The priority queue is a min_heap
    request_time_heap = Queue.PriorityQueue()

    # Parameter that keeps track of the simulation. Simulation is only over when all cars left GT
    simulation_active = True

    #Our time keeper variable
    time = 0

    #some constants
    timeToLeaveParkingLot = 15
    timeToEnterHighway = 40

    #While the simulation is running
    while simulation_active:

        #update all the requests
        update_heap


        # Check all nodes in the system first
        for Node in adj_list.keys():
            Node.time += 1

            #update the parking lot behavior: exit if possible and update capacity
            if Node.isParkingLot:
                #find the adjacent road
                adjacentInfo = adj_list[Node]
                adjacentEdge = adjacentInfo.values()
                #make sure the road is not full and that it's not too soon to leave
                if (not adjacentEdge.isFull()) and (Node.time % timeToLeaveParkingLot == 0):
                     adjacentEdge.currentCap += 1
                     Node.capacity -= 1
                     #reset the time.  15 seconds til the next car can leave
                     Node.time = 0

            #let the cars on the highway
            if Node.isExit:
                #find the adjacent road
                adjacentInfo = adj_list[Node]
                adjacentEdge = adjacentInfo.values()


            #If there are cars in the queue, process
            if Node.capacity !=0 :

                #Get all possible requests and compute the best heuristic at that time
                possible_requests = adj_list[Node]
                best_path = compute_heuristic(possible_requests) #Get the best path
                request_time_heap.put(best_path) #And put it in the  priority queue

                #Now update the heap based on the clock ticks:
                request_time_heap = update_heap(request_time_heap,clock_tick_time)

                #And get the values where the time request is 0
                update_adjacency_list(adj_list,request_time_heap)







    time += 1

def update_adjacency_list(adj_list,heap):
    pass


'''
Makes clock ticks in the heap
'''
def update_heap(request_time_heap, clock_tick_time):
    # Creating a list that stores all elements
    heap_list = []
    new_heap = Queue.PriorityQueue

    #Getting elements from the heap
    while len(request_time_heap) > 0:
        heap_list.append(request_time_heap.get())

    #And subtracting time from them
    for el in heap_list:
        el.time -= clock_tick_time
        if el.time <= 0:
            el = 0
        new_heap.put(el)
    return new_heap




def change_distribution(adj_list):
    pass



def compute_heuristic(request_dict,algorithm = "Police Officer"):
    '''

    :param request_dict:
    :param algorithm:
    :return: The best choice in that dictionary for that request
    '''
    if algorithm == "Police Officer":
        pass
    else:
        pass
