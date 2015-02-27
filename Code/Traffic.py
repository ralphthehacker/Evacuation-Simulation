import copy
from math import ceil, floor
import random
import threading
import numpy.random as np_random
import sys
from Node import createMap, workRequest
import time
__author__ = 'ralphblanes, lmoore44'
import Queue
import datetime


'''
This is the main simulation class. She'll take an adjacency list and run the simulation based on it.
You can also change the update time through the clock_tick_time parameter(default = 2s)
'''


def simulate(exit_list, enter_list, edgeList, parkingLots, algorithm, debug = False,clock_tick_time=2,output = 'Clean'):
    # Adjacency lists are stored in the form Node, {adjacent nodes, edge between them}


    '''
    TODO
    '''


    # We're putting all the requests in here to update them. The priority queue is a min_heap
    request_time_heap = Queue.PriorityQueue()

    # Parameter that keeps track of the simulation. Simulation is only over when all cars left GT
    simulation_active = True

    #Our time keeper variable
    iteration_timer = 0

    #some constants: in miliseconds
    timeToLeaveParkingLot = 10
    timeToEnterHighway = 20
    people_escaped = 0


    #Determining how many data displays we'll have
    update = 0
    for lot in parkingLots:
        update += lot.capacity
    #Basically just flooring to a a number in the format X000
    STARTING_CAPACITY = update
    update = 200*int(floor(float(update)/(10*len(str(update)))))


    #preprocessing step: Allows us to change the distribution of cars in an adjacency list
    change_distribution(parkingLots,exponential=True,sample_size= STARTING_CAPACITY)

    print "--------------------------------------------------------------------------------------------------------"
    print "OH NO, ZOMBIES ARE ATTACKING GEORGIA TECH!"
    time.sleep(1.5)
    print "WE NEED TO EVACUATE THE CAMPUS IMMEDIATELY!"
    time.sleep(1.5)
    ##ADD DISTRIBUTION RELATED TEXT IN HERE
    print "ARE YOU READY TO START?"
    time.sleep(1.5)
    print "--------------------------------------------------------------------------------------------------------"
    #While the simulation is running
    while simulation_active:
        if iteration_timer%update == 0:
            print "--------------------------------------------------------------------------------------------------------"
            m, s = divmod(iteration_timer/50, 60)
            h, m = divmod(m, 60)
            print "Zombie invasion started %d:%02d:%02d ago" % (h, m, s)
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

                #make sure the road is not full, there's cars in the parking lot, and that it's not too soon to leave
                if (not adjacentEdge.isFull()) and (Node.time <= 0) and Node.capacity:
                    #Move one car from the parking lot to its adjacent Node
                    adjacentEdge.currentCap += 1
                    Node.capacity -= 1
                    #reset the time.  0.1 seconds til the next car can leave
                    Node.time = 10

                else:
                    Node.time -= clock_tick_time

            #let the cars on the highway
            elif Node.isExit:


                #find the adjacent road
                adjacentInfo = enter_list[Node]
                #Get nodes connected to exit
                adjacentEdge = adjacentInfo.values()[0]

                #make sure the road has cars and that it's not too soon to leave
                if adjacentEdge.currentCap > 0:
                    if (Node.time <= 0):
                        #remove one car from the map
                        adjacentEdge.currentCap -= 1
                        Node.time = ceil(timeToEnterHighway - (timeToEnterHighway - 1) * (1 - (abs(adjacentEdge.currentCap) / adjacentEdge.capacity))) + 1
                    else:
                        Node.time -=  clock_tick_time
            #If there are cars in the queue, Make requests at a local heap



            #
            #Call heuristic to file work requests.
            # Then, we check to see if any work request can be fullfiled by "peeking" at the top of the heap and seeing if a time reaches zero
            # Assuming at least one does reach zero, we execute exactly one work request.
            # Don't forget to update all the work requests at each iteation by calling update_heap(or a modified version)
            #
            #Get the best choice for every path leading to the intersection
            else:
                bool = False
                roadsLeaving = exit_list[Node]
                carsEntering = enter_list[Node]

                #If the Node is not busy, we compute the heuristic for the best paths
                if len(Node.pastQueries) <= 0:
                    choiceList = compute_heuristic(carsEntering, roadsLeaving, algorithm,debug = bool)
                #Else, we process the current request
                else:
                    choiceList = Node.pastQueries
                # Get the possible choices and process them
                if choiceList:
                    for request in choiceList:
                        #Add to the heap
                        if are_the_queries_equal(Node,request):
                            #Debugging statement that covers against repeated equal requests
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


        #Check and count the number of people that are being harassed by zombies. If everyone escaped then the simulation is over
        people_in_sim = 0
        #The number of people in the simulation is the sum of all cars in the parking lots + people in the
        for edge in edgeList:
            people_in_sim += edge.currentCap
        for lot in parkingLots:
            people_in_sim += lot.capacity
        if people_in_sim <= 0:
            simulation_active = False

        #Provides data visualization
        if iteration_timer%update == 0:
            people_escaped = STARTING_CAPACITY - people_in_sim
            if output == 'Clean':
                monitor_nodes(edgeList,parkingLots,iteration_timer,people_escaped,STARTING_CAPACITY,clean = True)
            else:
                monitor_nodes(edgeList,parkingLots,iteration_timer,people_escaped,STARTING_CAPACITY,clean = False)

        # Keeps time running
        iteration_timer += clock_tick_time

    monitor_nodes(edgeList,parkingLots,iteration_timer,people_escaped,STARTING_CAPACITY,clean = False,endgame = True)



def monitor_nodes(edge_list,p_lots,iteration_timer,escaped,starting_pop,clean = True,endgame = False):
    #Pretty obvious code. Allows you to visualize the data
    #Clean just returns brief statements about the model's status

    if clean:
        num_people = 0
        for edge in edge_list:
            num_people += edge.currentCap
        for lot in p_lots:
            num_people += lot.capacity
        print"People left: ", num_people, ". And the time so far: ", iteration_timer, " seconds"

    else:
        print("*******************************************************************BRIEFING************************************************************************")
        print ""
        print("Total count of cars: {}".format(starting_pop - escaped))
        num_people = 0
        print("")
        print("*******************************************************************PARKING LOTS********************************************************************")
        print("")
        for lot in p_lots:
            print lot.name + ": " + str(lot.capacity)
            num_people += lot.capacity

        print("********************************************************************STREETS************************************************************************")
        print""
        for edge in edge_list:
            print repr(edge) + ": " + str(edge.currentCap)
            num_people += edge.currentCap

        print("********************************************************************STATUS************************************************************************")
        m, s = divmod(iteration_timer/50, 60)
        h, m = divmod(m, 60)
        print "Zombie invasion started %d:%02d:%02d ago" % (h, m, s)
        track = "%d HOURS,%02d MINUTES AND %02d SECONDS!" % (h, m, s)
        print ""
        if not endgame:
            print("THERE ARE {} PEOPLE STILL TRAPPED WITH THE ZOMBIES!".format(num_people))
        else:
            #Larry will probably hate this print statement :*
            print "CONGRATULATIONS! {} OF THE 21ST CENTURY'S FUTURE INNOVATORS ESCAPED THE FEROCIOUS ZOMBIES! ".format(starting_pop) +\
                "IN ONLY {}".format(track)
        print("")
    print("**************************************************************************************************************************************************")


    print("")


def change_distribution(parking_lots,exponential = False,sample_size = 100):
    #TODO MAKE AN EXPONENTIAL WHEN MY BRAIN RECOVERS FROM TODAY'S FRYING
    pass




def executeWorkRequestOrder(Node,order,debug = False):

    '''
    THIS IS USED TO DRIVE CARS FROM ONE STREET TO THE OTHER
    :param order:
    :return:
    '''

    #Covering against null orders
    if (order.edge1.currentCap == 0):
        Node.pastQueries.remove(order)
    #Debugging statement. Turn debug on if anything's getting messed up
    if debug:
        print "I got past the first two if statements"
    Node.pastQueries.remove(order)
    if debug:
        print("{} Order was removed: Successful traffic").format(order)
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

                if enter_road.currentCap > 0:
                    # Check the possible next paths for the least people in it
                    leastRatio = 1.0
                    best_exit = 0
                    n_cars = 0
                    for dest_road in roadsLeaving.values():
                        #check if the road is travellable
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
                        n_cars = best_exit.currentCap
                        for i in range(n_cars+1):
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
                if road.direction == "East" and eastRoadEligible(road):
                    canGoEast = True
                    eastRoad = road

            #If we can go East, then check if it's not full
            if canGoEast and not eastRoad.isFull():
                #Now we file a work request for each road
                for incomingCar in carsEntering.values():
                    if incomingCar.currentCap > 0:
                        work_list.append(workRequest(incomingCar, eastRoad))

            #check if we can't go east at all
            elif not canGoEast:
                numOptions = roadsLeaving.values()
                for car in carsEntering.values():
                    if car.currentCap > 0:
                        #randomely pick between north or south
                        exit = numOptions[random.randint(0,len(numOptions)-1)]
                        work_list.append(workRequest(car, exit))
                        #otherwise, we're done

        if not work_list:
            work_list = 0
        return work_list

    return 0

#checks if the road contains a parking lot, if it is full or if it's cycling back and forth
def roadEligible(dest_road,start_road):
    return not ( dest_road.startVertex.isParkingLot) and dest_road.currentCap < dest_road.capacity \
    and (start_road.startVertex.name != dest_road.endVertex.name)


def eastRoadEligible(dest_road):
    return not ( dest_road.endVertex.isParkingLot) and dest_road.currentCap < dest_road.capacity


def are_the_queries_equal(Node,work_request):
    #Checks if the queries in a node are equal ..... #noShitSherlock
    flag = False
    for requests in Node.pastQueries:
        if (requests.edge1 == work_request.edge1) and (requests.edge2 == work_request.edge2):
            flag = True
            return flag
    return flag







def main():
    n_people = 1000
    (exiting_list, entering_list, edge_list, parkingLots) = createMap("../GTMap.csv",n_people)
    simulate(exiting_list, entering_list, edge_list, parkingLots, "Greedy",debug=True,clock_tick_time=10
             ,output='dirty')#'dirty')
    (exiting_list, entering_list, edge_list, parkingLots) = createMap("../GTMap.csv",n_people)
    simulate(exiting_list, entering_list, edge_list, parkingLots, "UGA Officer",debug=True,clock_tick_time=10
             ,output='dirty')#'dirty')


main()

