import random
from Node import createMap, workRequest

__author__ = 'ralphblanes, lmoore44'
import Queue

'''
This is the main simulation class. She'll take an adjacency list and run the simulation based on it.
You can also change the update time through the clock_tick_time parameter(default = 2s)
'''


def simulate(exit_list, enter_list, edgeList, clock_tick_time=2, algorithm="Police Officers"):
    # Adjacency lists are stored in the form Node, {adjacent nodes, edge between them}


    '''
    TODO
    '''


    #preprocessing step: Allows us to change the distribution of cars in an adjacency list
    change_distribution(0)

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

        # Check all nodes in the system first
        for Node in exit_list.keys():
            print "Current Node is {}".format(Node)
            print "The current Node has the {} type".format(Node)
            Node.time += 1
            updateWorkRequests(Node)


            #update the parking lot behavior: exit if possible and update capacity
            if Node.isParkingLot:
                #find the adjacent road
                adjacentInfo = exit_list[Node]
                adjacentEdge = adjacentInfo.values()[0]

                #make sure the road is not full and that it's not too soon to leave
                if (not adjacentEdge.isFull()) and (Node.time % timeToLeaveParkingLot == 0):
                    adjacentEdge.currentCap += 1
                    Node.capacity -= 1
                    #reset the time.  15 seconds til the next car can leave
                    Node.time = 0

            #let the cars on the highway

            if Node.isExit:
                print "I am an exit"
                print "My name is {}".format(Node)

                #find the adjacent road
                adjacentInfo = enter_list[Node]
                #Get nodes connected to exit
                adjacentEdge = adjacentInfo.values()[0]

                #make sure the road is not full and that it's not too soon to leave
                if (not adjacentEdge.isFull()) and (Node.time % timeToEnterHighway == 0):
                    adjacentEdge.currentCap -= 1
                    #reset the time.  15 seconds til the next car can leave
                    Node.time = 0



            #If there are cars in the queue, Make requests at a local heap

            roadsLeaving = exit_list[Node]
            carsEntering = enter_list[Node]
            print "Those are getting inside of me".format(carsEntering)
            print("")
            print "I'm spitting these".format(roadsLeaving)

            """Call heuristic to file work requests.
            Then, we check to see if any work request can be fullfiled by "peeking" at the top of the heap and seeing if a time reaches zero
            Assuming at least one does reach zero, we execute exactly one work request.
            Don't forget to update all the work requests at each iteation by calling update_heap(or a modified version)
            """

            #Get the best choice for every path leading to the intersection(local optimi
            choiceList = compute_heuristic(carsEntering, roadsLeaving, algorithm)
            print ""
            print "My best choices are {}".format(choiceList)

            for request in choiceList:
                print( "I am a request and my name is {}".format(request))
                #Add to the heap
                Node.heap.put(request)

            #look at the heap contents

            #Then update time
            #look at the heap contents
            content = Node.heap.get()
            print("My cute tiny heap is {}".format(content))
            print ""
            print("Right now my time is {}".format(content.time))
            #if the time is equal to or less than zero, it's time to execute.  Else, put the order back in the queue
            if content.time <= 0:
                executeWorkRequestOrder(content)
            else:
                Node.heap.put(content)


                #check if we're empty
                allEmpty = True
            for edge in edgeList:
                if edge.capacity is not 0:
                    allEmpty = False
                if allEmpty:
                    simulation_active = False
            time += 1


'''
CHECK HERE FOR POSSIBLE BUGS. PYTHON may copy objects instead of keeping pointers
'''


def update_adjacency_list(adj_list, heap):
    pass


'''
Makes clock ticks in the heap
'''


def change_distribution(adj_list):
    pass


def executeWorkRequestOrder(order):
    print "Car going from {} to {}".format(order.edge1,order.edge2)
    order.edge1.currentCap -= 1
    order.edge2.currentCap += 1


def updateWorkRequests(Node):
    # Creating a list that stores all elements
    heap_list = []
    new_heap = Queue.PriorityQueue()
    request_time_heap = Node.heap

    # Getting elements from the heap
    while request_time_heap.qsize() > 0:
        heap_list.append(request_time_heap.get())

    #And subtracting time from them
    for el in heap_list:
        el.time -= 1
        if el.time <= 0:
            el = 0
        new_heap.put(el)
        # try:
        #     new_heap.put(el)
        # except:
        #
        #     # print ""
        #     # print "The element that fucked up was {}".format(el)
        #     # print "The new heap was:"
        #     # print new_heap
        #     # print "The old heap was:"
        #     # print Node.heap

    return new_heap


def compute_heuristic(carsEntering, roadsLeaving, algorithm="Police Officer"):
    '''

    :param request_dict:
    :param algorithm:
    :return: The best choice in that dictionary for that request
    '''

    if algorithm == "Police Officer":
        # Checking all possible paths
        work_list = []

        # For any given entering path
        for enter_road in carsEntering:
            temp_list = []

            # Check the possible next paths
            for destination_road in roadsLeaving:
                if destination_road.direction.lower() != "west":
                    #And issue work orders to them
                    work_order = workRequest(enter_road, destination_road)
                    temp_list.append(work_order)

            #Sort to get the fastest path
            temp_list = sorted(work_list, key=lambda x: x.time, reverse=False)

            #Get the fastest path and append it to the list of best choices
            work_list.append(temp_list[0])

        #and returning a list with the correspondent best values for each edge
        return work_list
    else:
        work_list = []
        # Greedy approach - people blindly try to go east.  Only go north or south if the east direction doesn't exist.
        #First determine if we can go East
        canGoEast = False
        for road in roadsLeaving.values():
            if road.direction == "East":
                canGoEast = True
                eastRoad = road

        #If we can go East, then check if it's not full
        if canGoEast and not eastRoad.isFull():
            #Now we file a work request for each road
            for incomingCar in carsEntering.values():
                work_list.append(workRequest(incomingCar, eastRoad))

        #check if we can't go east at all
        elif not canGoEast:
            numOptions = roadsLeaving.values()
            for incomingCar in carsEntering.values():
                #randomely pick between north or south

                # #class good_codingPractice()
                a = roadsLeaving.values()
                a = a[random.randint(0,len(numOptions)-1)]
                b = incomingCar
                work_list.append(workRequest(b, a))
                #otherwise, we're done




        return work_list


def main():
    (exiting_list, entering_list, edge_list) = createMap("../GTMap.csv")
    simulate(exiting_list, entering_list, edge_list, clock_tick_time=2)


main()