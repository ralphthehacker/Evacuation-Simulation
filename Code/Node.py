__author__ = 'ralphblanes'
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


        end_coords = (traffic_obj['X2'],traffic_obj['Y2'])
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
    :param Start point and end point of the object, type of the object
    '''
    def __init__(self, start_coords, end_coords,type):
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.type = type

        self.resource = None #SIMPY RESOURCE CREATION GOES HERE

        #have a field for whether it's an intersection or a parking lot
        #have a field for capacity 



#Change this
createMap("/Users/ralphblanes/Documents/Computer Simulation(Vuduc)/Evacuation Simulation/Data/gtmap.csv")