__author__ = 'ralphblanes, lawrencemoore'
#from SimPy.Simulation import *
import pandas
from Queue import PriorityQueue

def createMap(filepath):

    #parking lot nodes always ".parking" in the name

    #Processing data into a dataframe
    df = pandas.read_csv(filepath)

    print df.columns.values

    #Looping through dataframes
    for index,traffic_obj in df.iterrows():

        #Let's append all intersections to a dictionary(hashmap) and then give them to the GT MAP
        intersections = {}

        #Getting intersection data and info
        inter1 = traffic_obj['NameOfIntersection1']
        inter2 = traffic_obj['NameOfIntersection2']
        distance_between_nodes = traffic_obj['Distance']
        direction = traffic_obj['Direction']
        forwardEdge = Edge_Queues()

        type = traffic_obj['Type']



        return



class Campus_Map:
    def __init__(self, intersections_list, parking_lots,):
        pass


class Edge_Queues:
     #direction is from the starting node to the end node
     #capacity is distance (in yards) divided by the length of the average car ( which is 4.5)
     def __init__(self, startVertex, endVertex, distance, direction):
          self.startVertex = startVertex
          self.endVertex = endVertex
          self.direction = direction
          self.capacity = distance / 4.5

class Map_node:

    '''
    Class: Map_node
    Description: contains a node that represents a Resource in the Georgia Tech Map. Resources can be either parking lots
    or traffic light intersections
    :param name
    '''

    def __init__(self, name):
        self.name = name
        self.isParkingLot = False
        #store heap
        self.heap = PriorityQueue(0)
        #have a field for whether it's an intersection or a parking lot
        #have a field for capacity 

class Parking_lot(Map_node):

     def __init__(self, name, capacity):
          self.isParkingLot = True
          self.capacity = capacity


createMap("../GTMap.csv")