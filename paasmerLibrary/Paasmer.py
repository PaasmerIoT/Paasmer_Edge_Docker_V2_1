import paho.mqtt.client as mqtt
import time
import json
client = mqtt.Client()

class Paasmer:
	host = ""
	feedSubscription = {}
	feedMonitorCB = {}
	def connect(self):
		client.on_connect = self.on_connect
        	client.on_message = self.on_message
		client.connect(self.host, 1883, 60)
	def on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		#client.subscribe("docker")
		client.subscribe("toSensor")
	def on_message(self,client, userdata, msg):
		subscribeMsg = (msg.payload)
		print(subscribeMsg)
		message = json.loads(subscribeMsg)
		if "feedControl" in message.keys():
			myFeed = message["feedControl"]["feedName"]
			myStatus = message["feedControl"]["value"]
			if myFeed in self.feedSubscription:
				self.feedSubscription[myFeed](myStatus)
				self.publish(myFeed,myStatus)
		'''
		for i in range(0, len(subscribeMsg)):
			if subscribeMsg[i] == ' ':
				myFeed = subscribeMsg[0:i]
				myStatus = subscribeMsg[i+1:len(subscribeMsg)]
				if myFeed in self.feedSubscription:
					self.feedSubscription[myFeed](myStatus)
					if myStatus == "on":
						self.publish(myFeed,1,"actuator")
					else:
						self.publish(myFeed,0,"actuator")
		'''
	def loop_start(self):
		client.loop_start()
	def subscribe(self,feed,cb):
		if feed not in self.feedSubscription:
			self.feedSubscription[feed] = cb
			self.publish(feed,0)
	def publish(self,feedName,feedValue,analytics = "none",analyticsCondition = "10"):
			#feedArray = []
			feedDetails = {}
			feedDetails["feedname"] = feedName
			'''
			if analytics == "aggregate":
				feedDetails["feedtype"] = "sensor_EA_Aggregate"
			elif analytics == "average":
				feedDetails["feedtype"] = "sensor_EA_Average"
			else:
				feedDetails["feedtype"] = feedType
			'''
			#feedDetails["feedpin"] = "1"
			feedDetails["feedvalue"] = str(feedValue)
			#feedDetails["ConnectionType"] = "MQTT"
			feedDetails["analytics"] = analytics
			feedDetails["analyticsCondition"] = analyticsCondition
			feedDetails["readings"] = "NULL"
			#feedArray.append(feedDetails)
			finalData = {}
			finalData["feeds"] = feedDetails
			message = json.dumps(finalData)
			if analytics == "none":
				client.publish("toAWS",message)
			else:
				client.publish("fromSensor",message)
	def ML_config(self,feedName,modelName):
		mlData = {}
		mlData["feedname"] = feedName
		mlData["name"] = modelName
		mlData["action"] = "config"
		message = json.dumps(mlData)
		client.publish("toML",message)
	def ML_predict(self,feedName,modelName,data = {}):
		mlData = {}
                mlData["feedname"] = feedName
                mlData["name"] = modelName
                mlData["action"] = "predict"
		mldata = {}
		for i in data.keys():
			#print i
			mlValue = []
			mlValue.append(data[i])
			mldata[i] = mlValue
		mlData["data"] = mldata
                message = json.dumps(mlData)
                client.publish("toML",message)
