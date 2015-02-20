__author__ = 'ralphblanes, lawrencemoore'
#from SimPy.Simulation import *
import pandas
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

        type = traffic_obj['Type']




        return



class Campus_Map:
    def __init__(self, intersections_list,parking_lots,):
        pass


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

        #have a field for whether it's an intersection or a parking lot
        #have a field for capacity 

class Parking_lot(Map_node):

     def __init__(self, name, capacity):
          self.isParkingLot = True
          self.capacity = capacity


#Change this
createMap("../GTMap.csv")