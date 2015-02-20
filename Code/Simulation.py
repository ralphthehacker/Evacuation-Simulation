__author__ = 'ralphblanes'
import simpy

def first_process(env,location):

    print ""
    print "Your car is stuck at traffic"
    event = simpy.events.Timeout(env, delay=1, value=42)
    print "Your car left traffic"
    value = yield event
    print('now=%d, value=%d' % (env.now, value))



env = simpy.Environment()
location_list = range(10,21)
for i in range(10):
    process_gen = first_process(env)
    p = simpy.events.Process(env, process_gen)

env.run()