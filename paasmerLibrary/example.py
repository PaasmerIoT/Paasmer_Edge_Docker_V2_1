from Paasmer import *
import time

#Callback functions for subscribed feeds
def feed1_CB(name):
	print("This is in feed4")
	print(name)
def feed2_CB(name):
	print("This is in feed7")
	print(name)
def feed3_CB(name):
	print("it is feed33")
	print(name)

###connecting to the Paasmer Edge docker device
paasmer = Paasmer()
paasmer.host = "localhost"   #IP address of the Paasmer Edge docker device.
paasmer.connect()

#subscribing to the feeds with callback functions
paasmer.subscribe("Act1",feed1_CB)
paasmer.subscribe("Act2",feed2_CB)
paasmer.subscribe("Act3",feed3_CB)

#loop start
paasmer.loop_start()

#configuring the ML with model name, which already created in paasmer cloud platform

paasmer.ML_config(feedName = "mlfeed",modelName = "Demo2")

while True:

	#publishing the feed details to Paasmer Edge docker device
	'''
	you can use the following analytics
	1.filter
	2.aggregate
	3.feedMonitoring
	4.average

	for filter, provide the analytics condition like "function(x) x < 5.0"

	for aggrgate, provide the number of values you want to do aggregate

	for average, provide the number of values you want to do average
	'''


	#publishing the feed details with filter analytics 
	paasmer.publish("feed5",feedValue = 2,analytics = "filter",analyticsCondition="function(x) x > 3.0")
	time.sleep(2)

	
	#publishing the feed details without any analytics 
	paasmer.publish("feed6",feedValue = 70)
	time.sleep(2)

	
	#publishing the feed details with aggregate analytics
	paasmer.publish("feed1",feedValue = 10,analytics = "aggregate",analyticsCondition = "3")
	time.sleep(2)

	#publishing the feed details with feedMonitoring
	paasmer.publish("feed3",feedValue = 10,analytics = "feedMonitoring")
	time.sleep(2)

	#publishing the feed details with average analytics
        paasmer.publish("feed2",feedValue = 350,analytics = "average",analyticsCondition = "12")
        time.sleep(2)

	#predicting the ml output by giving input
	paasmer.ML_predict(feedName = "mlfeed",modelName = "Demo2",data = {"eng":29,"lang":27,"maths":15,"sci":25,"soc":31})

	#publishing the feed details with average analytics
        paasmer.publish("feed8",feedValue = 70,analytics = "average",analyticsCondition = "10")
        time.sleep(2)

	#publishing the feed details without any analytics
        paasmer.publish("feed9",feedValue = 55)
        time.sleep(2)
	
	#publishing the feed details with feedMonitoring
        paasmer.publish("feed10",feedValue = 90,analytics = "feedMonitoring")
        time.sleep(2)

