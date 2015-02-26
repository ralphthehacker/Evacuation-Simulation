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


def simulate(exit_list, enter_list, edgeList, parkingLots, algorithm, debug = False,clock_tick_time=2,output = 'Clean'):
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
        if time%500 == 0:
            print "--------------------------------------------------------------------------------------------------------"
            print "new iteration"
            print time
            print "--------------------------------------------------------------------------------------------------------"
        # Check all nodes in the system first
        for Node in exit_list.keys():

            #update the time of all the work requests
            updateWorkRequests(Node,clock_tick_time)


            #update the parking lot behavior: exit if possible and update capacity
            if Node.isParkingLot and Node.capacity > 0:
                if Node.time == 0:
                    a = 0
                #find the adjacent road
                adjacentInfo = exit_list[Node]
                adjacentEdge = adjacentInfo.values()[0]
                adjacent_edge_is_full = adjacentEdge.isFull()
                if Node.name == "KlausStop" and len(Node.pastQueries)>0:
                    a = 0

                #make sure the road is not full, there's cars in the parking lot, and that it's not too soon to leave
                if (not adjacentEdge.isFull()) and (Node.time <= 0) and Node.capacity:
                    adjacentEdge.currentCap += 1
                    Node.capacity -= 1
                    #reset the time.  15 seconds til the next car can leave
                    Node.time = 10
                    print("A car just left the parking lot")
                else:
                    Node.time -= clock_tick_time

            #let the cars on the highway
            elif Node.isExit:
                # print "I am an exit"
                # print "My name is {}".format(Node)

                #find the adjacent road
                adjacentInfo = enter_list[Node]
                #Get nodes connected to exit
                adjacentEdge = adjacentInfo.values()[0]

                #make sure the road has cars and that it's not too soon to leave
                if adjacentEdge.currentCap > 0:
                    if (Node.time <= 0):
                        print "A car just exited"
                        adjacentEdge.currentCap -= 1
                        #The more crowded the road, the long it takes to exit
                        Node.time = ceil(timeToEnterHighway - (timeToEnterHighway - 1) * (1 - (abs(adjacentEdge.currentCap) / adjacentEdge.capacity))) + 1
                    else:
                        Node.time -=  clock_tick_time
            #If there are cars in the queue, Make requests at a local heap


            # print "Those are getting inside of me".format(carsEntering)
            # print("")
            # print "I'm spitting these".format(roadsLeaving)
            #
            # """Call heuristic to file work requests.
            # Then, we check to see if any work request can be fullfiled by "peeking" at the top of the heap and seeing if a time reaches zero
            # Assuming at least one does reach zero, we execute exactly one work request.
            # Don't forget to update all the work requests at each iteation by calling update_heap(or a modified version)
            # """
            #Get the best choice for every path leading to the intersection(local optimi
            else:
                if Node.name == "Centinial" and time >= 2000:
                    breakpoint = "AQUI CARALHO"
                bool = False
                roadsLeaving = exit_list[Node]
                carsEntering = enter_list[Node]

                #If the Node is not busy, we compute the heuristic for the best paths
                if len(Node.pastQueries) <= 0:
                    choiceList = compute_heuristic(carsEntering, roadsLeaving, algorithm,debug = bool)
                #Else, we process the current request
                else:
                    #Debugging heuristic
                    if Node.name == "Centinial" and time >= 2500:
                        bool = False
                        for car in carsEntering.values():
                            if car.currentCap > 0:
                                bool = True
                        if bool:
                            breakpoint = "AQUI DE NOVO PORRA"

                    choiceList = Node.pastQueries
                #if there is no possible way of moving, no choice list will be generated
                if choiceList:
                    for request in choiceList:
                        """
                        TODO:   Cars are either getting stuck on exit without being processed or they are getting
                        back to the parking lots and getting stuck
                        """
                        #Add to the heap
                        if are_the_queries_equal(Node,request):
                            breakpoint = "another"
                        elif request.edge1.currentCap > 0 :
                            Node.pastQueries.append(request)
                            Node.heap.put(request)

                    #look at the top work order and see if it's time is zero (aka execute it)
                    content = Node.heap.get()

                    #if the time is equal to or less than zero, it's time to execute.  Else, put the order back in the queue
                    if content is not None and content.time <= 0 :
                        executeWorkRequestOrder(Node,content)

                    else:
                        Node.heap.put(content)

        if time%500 == 0:
            if output == 'Clean':
                monitor_nodes(edgeList,parkingLots,time,clean = True)
            else:
                monitor_nodes(edgeList,parkingLots,time,clean = False)
        #check if we're empty
        numPeople = 0
        # for edge in edgeList:
        #     if '.EXIT' in edge.endVertex.name and edge.currentCap != 0:
        #         edge.currentCap -= 1
        #         print 'A car just left GT through {}'.format(edge)


        for edge in edgeList:
            numPeople += edge.currentCap
        for lot in parkingLots:
            numPeople += lot.capacity
        if numPeople <= 0:
            simulation_active = False

        if time == 0:
            print"People left: ", numPeople, ". And the time so far: ", time, " seconds"
        time += clock_tick_time
    print time

'''
CHECK HERE FOR POSSIBLE BUGS. PYTHON may copy objects instead of keeping pointers
'''


'''
Makes clock ticks in the heap
'''



def monitor_nodes(edge_list,p_lots,time,clean = True):
    if clean:
        num_people = 0
        for edge in edge_list:
            num_people += edge.currentCap
        for lot in p_lots:
            num_people += lot.capacity
        print"People left: ", num_people, ". And the time so far: ", time, " seconds"

    else:
        print("*******************************")
        print("Total count of cars:")
        num_people = 0
        print("")
        print("*******************************")
        for lot in p_lots:
            print lot.name + ": " + str(lot.capacity)
            num_people += lot.capacity

        print("*******************************")
        for edge in edge_list:
            print repr(edge) + ": " + str(edge.currentCap)
            num_people += edge.currentCap

        print("*******************************")
        print ""
        print("THERE ARE {} PEOPLE IN THE SYSTEM!".format(num_people))
        print("")
    print("*******************************")


    print("")


def change_distribution(adj_list):
    pass


def executeWorkRequestOrder(Node,order,debug = False):

    '''
    THIS IS USED TO DRIVE CARS FROM ONE STREET TO THE OTHER
    :param order:
    :return:
    '''

    #print "Car going from {} to {}".format(order.edge1,order.edge2)
    if (order.edge1.currentCap == 0):
        #print("")
        #print "work request coming from a road with zero cars"
        Node.pastQueries.remove(order)
    # if (order.edge2.currentCap == 0 and not(order.edge1.startVertex.isParkingLot)):
    #     #print("")
    #     #print "work request coming from a road with zero cars"
    #     Node.pastQueries.remove(order)
    #     if debug:
    #         print("{} Order was removed: null").format(order)
    #         print "{} is returning here".format(order)
    #     return
    # if ('.EXIT' in order.edge2.name):
    #     print  "{} just arrived in an exit".format(order)
    # if ('.parking' in order.edge2.name):
    #     print  "{} just backtracked to a parking lot".format(order)
    if debug:
        print "I got past the first two if statements"
    Node.pastQueries.remove(order)
    if debug:
        print("{} Order was removed: Sucessful traffic").format(order)
    order.edge1.currentCap -= 1
    order.edge2.currentCap += 1


def updateWorkRequests(Node,clock):

    '''
    THIS IS USED TO LOOK INTO EVERY SINGLE INDIVIDUAL HEAP AND POP THE ORDERS
:param Node:
:param clock:
:return:
'''
    #make sure there's at least one element in the heap
    if Node.heap.queue:
        heap_list = []
        # Getting elements from the heap
        while Node.heap.qsize() > 0:
            heap_list.append(Node.heap.get())

        #And subtracting time from them
        for order in heap_list:
            order.time -= clock
            if order.time <= 0:
                order.time = 0

            Node.heap.put(order)


def compute_heuristic(carsEntering, roadsLeaving, algorithm,debug = False):
    '''

    :param request_dict:
    :param algorithm:
    :return: The best choice in that dictionary for that request
    '''

    #Possible bug in here
    if not carsEntering.values()[0].endVertex.isExit:
        """the above condition checks if we're at the exit.  If so, no intersection guidance is needed; it will be picked up by the clock cycle
        also, check to see if the road you choose is full"""

        for key in roadsLeaving.keys():
            if key.isParkingLot:
                del roadsLeaving[key]
        if algorithm == "UGA Officer":
            # Checking all possible paths
            work_list = []
            # For any given entering path
            for enter_road in carsEntering.values():
                #make sure the road isn't empty
                #debug if
                if enter_road.currentCap < 0:
                    print "the problem starts here"

                elif enter_road.currentCap > 0:


                    # Check the possible next paths for the least people in it
                    leastRatio = 1.0
                    best_exit = 0
                    for dest_road in roadsLeaving.values():
                        #check if the raod is
                        if dest_road.direction.lower() != "west" and roadEligible(dest_road,enter_road):
                            #check if this road is less empty. This calculation prefers longer, emptier roads
                            if dest_road.currentCap/dest_road.capacity < leastRatio:
                                best_exit = dest_road
                                leastRatio = dest_road.currentCap/dest_road.capacity
                            #And issue work orders to them
                            elif dest_road.currentCap/dest_road.capacity == leastRatio:
                                coin = random.random()
                                if coin > 0.50:
                                    best_exit = dest_road
                                else:
                                    best_exit = best_exit


                    #Get the fastest path (assuming one exists) and append it to the list of best choices
                    if best_exit:
                        minRequest = workRequest(enter_road, best_exit)
                        work_list.append(minRequest)
                elif enter_road.currentCap < 0:
                    print "negative car capacity"
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
def roadEligible(dest_road,start_road):
    return not ( dest_road.startVertex.isParkingLot) and dest_road.currentCap < dest_road.capacity \
    and (start_road.startVertex.name != dest_road.endVertex.name)





def are_the_queries_equal(Node,work_request):
    #Checks if the queries in a node are equal
    flag = False
    for requests in Node.pastQueries:
        if (requests.edge1 == work_request.edge1) and (requests.edge2 == work_request.edge2):
            flag = True
            return flag
    return flag







def main():
    (exiting_list, entering_list, edge_list, parkingLots) = createMap("../GTMap.csv")
    #simulate(exiting_list, entering_list, edge_list, parkingLots, "chaos", clock_tick_time=2)
    simulate(exiting_list, entering_list, edge_list, parkingLots, "UGA Officer",debug=True,clock_tick_time=10
             ,output='dirty')#'dirty')


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