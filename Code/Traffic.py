from math import ceil
import random
import sys
from Node import createMap, workRequest

__author__ = 'ralphblanes, lmoore44'
import Queue

'''
This is the main simulation class. She'll take an adjacency list and run the simulation based on it.
You can also change the update time through the clock_tick_time parameter(default = 2s)
'''


def simulate(exit_list, enter_list, edgeList, parkingLots, algorithm, clock_tick_time=2):
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
    timeToLeaveParkingLot = 10
    timeToEnterHighway = 20

    #While the simulation is running
    while simulation_active:

        # Check all nodes in the system first
        for Node in exit_list.keys():
            #update the time of all the work requests
            updateWorkRequests(Node)


            #update the parking lot behavior: exit if possible and update capacity
            if Node.isParkingLot:
                #find the adjacent road
                adjacentInfo = exit_list[Node]
                adjacentEdge = adjacentInfo.values()[0]

                #make sure the road is not full, there's cars in the parking lot, and that it's not too soon to leave
                if (not adjacentEdge.isFull()) and (Node.time % timeToLeaveParkingLot == 0) and Node.capacity:
                    adjacentEdge.currentCap += 1
                    Node.capacity -= 1
                    #reset the time.  15 seconds til the next car can leave
                    Node.time = 1
                else:
                    Node.time += 1

            #let the cars on the highway

            if Node.isExit:
                # print "I am an exit"
                # print "My name is {}".format(Node)

                #find the adjacent road
                adjacentInfo = enter_list[Node]
                #Get nodes connected to exit
                adjacentEdge = adjacentInfo.values()[0]

                #make sure the road has cars and that it's not too soon to leave
                if adjacentEdge.currentCap > 0:
                    if (Node.time == 0):
                        adjacentEdge.currentCap -= 1
                        #The more crowded the road, the long it takes to exit
                        Node.time = ceil(timeToEnterHighway - (timeToEnterHighway - 1) * (1 - (abs(adjacentEdge.currentCap) / adjacentEdge.capacity))) + 1
                    else:
                        Node.time -= 1


            #If there are cars in the queue, Make requests at a local heap

            roadsLeaving = exit_list[Node]
            carsEntering = enter_list[Node]
            # print "Those are getting inside of me".format(carsEntering)
            # print("")
            # print "I'm spitting these".format(roadsLeaving)

            """Call heuristic to file work requests.
            Then, we check to see if any work request can be fullfiled by "peeking" at the top of the heap and seeing if a time reaches zero
            Assuming at least one does reach zero, we execute exactly one work request.
            Don't forget to update all the work requests at each iteation by calling update_heap(or a modified version)
            """

            #Get the best choice for every path leading to the intersection(local optimi
            if not Node.isParkingLot:
                choiceList = compute_heuristic(carsEntering, roadsLeaving, algorithm)
                #if there is no possible way of moving, no choice list will be generated
                if choiceList:
                    for request in choiceList:
                        #Add to the heap
                        Node.heap.put(request)

                    #look at the top work order and see if it's time is zero (aka execute it)
                    content = Node.heap.get()

                    #if the time is equal to or less than zero, it's time to execute.  Else, put the order back in the queue
                    if content.time <= 0:
                        executeWorkRequestOrder(content)

                    else:
                        Node.heap.put(content)


        #check if we're empty
        numPeople = 0
        for edge in edgeList:
            numPeople += edge.currentCap
        for lot in parkingLots:
            numPeople += lot.capacity
        if numPeople <= 0:
            simulation_active = False


        print"People left: ", numPeople, ". And the time so far: ", time, " seconds"
        time += 1
    print time

'''
CHECK HERE FOR POSSIBLE BUGS. PYTHON may copy objects instead of keeping pointers
'''


'''
Makes clock ticks in the heap
'''


def change_distribution(adj_list):
    pass


def executeWorkRequestOrder(order):
    #print "Car going from {} to {}".format(order.edge1,order.edge2)
    order.edge1.currentCap -= 1
    order.edge2.currentCap += 1


def updateWorkRequests(Node):

    #make sure there's at least one element in the heap
    if Node.heap.queue:
        heap_list = []
        # Getting elements from the heap
        while Node.heap.qsize() > 0:
            heap_list.append(Node.heap.get())

        #And subtracting time from them
        for order in heap_list:
            order.time -= 1
            if order.time <= 0:
                order.time = 0

            Node.heap.put(order)


def compute_heuristic(carsEntering, roadsLeaving, algorithm):
    '''

    :param request_dict:
    :param algorithm:
    :return: The best choice in that dictionary for that request
    '''
    if not carsEntering.values()[0].endVertex.isExit:
        """the above condition checks if we're at the exit.  If so, no intersection guidance is needed; it will be picked up by the clock cycle
        also, check to see if the road you choose is full"""

        if algorithm == "Police Officer":
            # Checking all possible paths
            work_list = []

            # For any given entering path
            for enter_road in carsEntering.values():
                #make sure the road isn't empty
                if enter_road.currentCap > 0:

                    # Check the possible next paths for the least people in it
                    leastRatio = 1.0
                    bestExit = 0
                    for dest_road in roadsLeaving.values():
                        #check if the raod is
                        if dest_road.direction.lower() != "west" and roadEligible(dest_road):
                            #check if this road is less empty
                            if dest_road.currentCap/dest_road.capacity < leastRatio:
                                bestExit = dest_road
                                leastRatio = dest_road.currentCap/dest_road.capacity
                            #And issue work orders to them

                    #Get the fastest path (assuming one exists) and append it to the list of best choices
                    if bestExit:
                        minRequest = workRequest(enter_road, bestExit)
                        work_list.append(minRequest)

        else:
            work_list = []
            # Greedy approach - people blindly try to go east.  Only go north or south if the east direction doesn't exist.
            #First determine if we can go East
            canGoEast = False
            for road in roadsLeaving.values():
                if road.direction == "East" and roadEligible(road):
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
                for car in carsEntering.values():
                    if car.capacity > 0:

                        #randomely pick between north or south
                        exit = numOptions[random.randint(0,len(numOptions)-1)]
                        work_list.append(workRequest(car, exit))
                        #otherwise, we're done

        if not work_list:
            work_list = 0
        return work_list

    return 0

#checks if the road contains a parking lot or is full
def roadEligible(road):
    return not ( road.startVertex.isParkingLot) and road.currentCap < road.capacity

def main():
    (exiting_list, entering_list, edge_list, parkingLots) = createMap("../GTMap.csv")
    #simulate(exiting_list, entering_list, edge_list, parkingLots, "chaos", clock_tick_time=2)
    simulate(exiting_list, entering_list, edge_list, parkingLots, "Police Officer", clock_tick_time=2)


main()


 #         work_order = workRequest(enter_road, dest_road)
                #         temp_list.append(work_order)
                #
                # #Sort to get the fastest path
                # #temp_list = sorted(work_list, key=lambda x: x.time, reverse=False)
                # minTime = sys.maxint
                # minRequest = 0
                # for request in temp_list:
                #     if request.time < minTime:
                #         minTime = request.time
                #         minRequest = request
                # if not minRequest:
                #     print False