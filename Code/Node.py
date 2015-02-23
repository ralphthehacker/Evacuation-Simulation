from math import ceil

__author__ = 'ralphblanes, lawrencemoore'
#from SimPy.Simulation import *
import pandas
from Queue import PriorityQueue
from random import randint

def createMap(filepath):
    #parking lot nodes always ".parking" in the name

    #Processing data into a dataframe
     df = pandas.read_csv(filepath)

     print df.columns.values
     exitingList = {}
     enteringList = {}
     vertexList = {}
     parkingLots = []
     edgeList = []
     #Looping through dataframes
     for index, traffic_obj in df.iterrows():
        #Let's append all intersections to a dictionary(hashmap) and then give them to the GT MAP

        #Getting intersection data and info
        inter1 = traffic_obj['NameOfIntersection1']
        inter2 = traffic_obj['NameOfIntersection2']
        distance = traffic_obj['Distance']
        direction = traffic_obj['Direction']


        #check if we've seen the vertex before
        if inter1 not in vertexList:
             #create the vertexes
             if ".parking" in inter1:
                  #randomely generate a certain number of cars in each parking lot
                  vert1 = Parking_lot(inter1, randint(2, 3))
                  parkingLots.append(vert1)
             elif ".EXIT" in inter1:
                  vert1 = Node(inter1, True)
             else:
                  vert1 = Node(inter1, False)

             vertexList[inter1] = vert1
        else:
             vert1 = vertexList[inter1]

        #repeat the process for the other vertexes
        if inter2 not in vertexList:
            if ".parking" in inter2:
                vert2 = Parking_lot(inter2, randint(2, 3))
                parkingLots.append(vert2)
            elif ".EXIT" in inter2:
                 vert2 = Node(inter2, True)
            else:
                 vert2 = Node(inter2, False)
            vertexList[inter2] = vert2
        else:
            vert2 = vertexList[inter2]


        forwardEdge = Edge(vert1, vert2, distance, direction)
        backwardsEdge = Edge(vert2, vert1, distance, flipDirection(direction))
        edgeList.append(forwardEdge)
        edgeList.append(backwardsEdge)

        """Make a dictionary with the key equal the vertex, and value equal to another dictionary.
           The dictionary representing the value stores adjacent vertexes as the key and their edge as the value
        """

        if vert1 not in exitingList.keys():
            #make the new exit dictionary
            new_exit_dictionary = {}
            new_exit_dictionary[vert2] = forwardEdge

            #make the new enter dictionary
            new_enter_dictionary = {}
            new_enter_dictionary[vert2] = backwardsEdge

            exitingList[vert1] = new_exit_dictionary
            enteringList[vert1] = new_enter_dictionary
        else:
            #deal with the exit list first
            current_dictionary = exitingList[vert1]
            current_dictionary[vert2] = forwardEdge
            exitingList[vert1] = current_dictionary

            #now deal with the entering list
            current_dictionary = enteringList[vert1]
            current_dictionary[vert2] = backwardsEdge
            enteringList[vert1] = current_dictionary


        """do the same in the inverse direction"""
        if vert2 not in exitingList.keys():
            #make the new exit dictionary
            new_exit_dictionary = {}
            new_exit_dictionary[vert1] = backwardsEdge

            #make the new enter dictionary
            new_enter_dictionary = {}
            new_enter_dictionary[vert1] = forwardEdge

            exitingList[vert2] = new_exit_dictionary
            enteringList[vert2] = new_enter_dictionary
        else:
            #deal with the exit list first
            current_dictionary = exitingList[vert2]
            current_dictionary[vert1] = backwardsEdge
            exitingList[vert2] = current_dictionary

            #now deal with the entering list
            current_dictionary = enteringList[vert2]
            current_dictionary[vert1] = forwardEdge
            enteringList[vert2] = current_dictionary

     return exitingList,enteringList,edgeList, parkingLots



class Edge:
     #direction is from the starting node to the end node
     #capacity is distance (in yards) divided by the length of the average car ( which is 4.5)
     def __init__(self, startVertex, endVertex, distance, direction):
          self.startVertex = startVertex
          self.endVertex = endVertex
          self.direction = direction
          self.capacity = ceil(int(distance) / 4.5)
          self.currentCap = 0

     def isFull(self):
          return self.currentCap == self.capacity
     def __repr__(self):
        return self.startVertex.name + " to " + self.endVertex.name

class Node:

    '''
    Class: Map_node
    Description: contains a node that represents a Resource in the Georgia Tech Map. Resources can be either parking lots
    or traffic light intersections
    :param name
    '''

    def __init__(self, name, isExit):
        self.name = name
        self.isParkingLot = False
        self.isExit = isExit
        self.heap = PriorityQueue(0)
        self.pastQueries = []
        self.time = 0
    def __repr__(self):
        return self.name
class Parking_lot(Node):

     def __init__(self, name, capacity):
          self.name = name
          self.isParkingLot = True
          self.capacity = capacity
          self.time = 0
          self.heap = PriorityQueue(0)
          self.isExit = False


def flipDirection(direction):
     if (direction == "West"):
          return "East"
     elif (direction == "East"):
          return "West"
     elif (direction == "North"):
          return "South"
     else:
          return "North"

class workRequest:
     #by default, car goes from edge 1 to edge 2.  Remember, this won't be generated if edge 2 has no capacity
     def __init__(self,edge1, edge2):
          self.edge1 = edge1
          self.edge2 = edge2
          self.time = 20 + edge1.currentCap/edge1.capacity
     def __cmp(self,other):
     	return cmp(self.time,other.time)
     def __repr__(self):
         return repr(self.edge1) + " and " + repr(self.edge1) + " with time of {}".format(self.time)

adj_list = createMap("../GTMap.csv")