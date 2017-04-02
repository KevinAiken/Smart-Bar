import bluetooth
import time
import serial
from time import sleep
import sys
zs = []
ser = serial.Serial('/dev/ttyACM0')


reps_needed = 100
reps_completed = 0

	
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)



port = 1
server_socket.bind(("",port))
server_socket.listen(1)
client_socket, address = server_socket.accept()
print "Accepted connection from: ", address

while True: # one loop per set

	#reps_needed = client_socket.recv(1024)

	
	if(reps_needed != 0):
		print "hey"
		reps_completed = 0
		balanced = 0
		while(reps_completed < reps_needed):  # one loop per set
			
			zeroes = 0
			intakeString = ser.readline()
			ardList = (ser.readline()).strip().split()

			heading = float(ardList[0])
			pitch = float(ardList[1])
			roll = float(ardList[2])
			
			x = float(ardList[3])
			y = float(ardList[4])
			z = float(ardList[5])
			
			if(pitch < -30):
				balanced = -1
			elif(pitch > 30):
				balanced = 1
			while( z < 1.15): #wait for start
				intakeString = ser.readline()
				ardList = (ser.readline()).strip().split()

				heading = float(ardList[0])
				pitch = float(ardList[1])
				roll = float(ardList[2])
				
				x = float(ardList[3])
				y = float(ardList[4])
				z = float(ardList[5])
				if(pitch < -30):
					balanced = -1
				elif(pitch > 30):
					balanced = 1
			t0 = time.time()
			while (z > 1.15):
				
				intakeString = ser.readline()
				ardList = (ser.readline()).strip().split()

				heading = float(ardList[0])
				pitch = float(ardList[1])
				roll = float(ardList[2])
				
				x = float(ardList[3])
				y = float(ardList[4])
				z = float(ardList[5])
				if(pitch < -30):
					balanced = -1
				elif(pitch > 30):
					balanced = 1
			while (z < 1.17):
				intakeString = ser.readline()
				ardList = (ser.readline()).strip().split()

				heading = float(ardList[0])
				pitch = float(ardList[1])
				roll = float(ardList[2])
				
				x = float(ardList[3])
				y = float(ardList[4])
				z = float(ardList[5])
				if(pitch < -30):
					balanced = -1
				elif(pitch > 30):
					balanced = 1
			while(z > 1.15):
				
				intakeString = ser.readline()
				ardList = (ser.readline()).strip().split()

				heading = float(ardList[0])
				pitch = float(ardList[1])
				roll = float(ardList[2])
				
				x = float(ardList[3])
				y = float(ardList[4])
				z = float(ardList[5])
				if(pitch < -30):
					balanced = -1
				elif(pitch > 30):
					balanced = 1
			t1 = time.time()
			reps_completed += 1
			print "Rep Completed"
			print "Time:"
			print t1-t0
			time_ms = int((t1-t0)*1000)
			
			print balanced
			bluetooth_message = str(time_ms) + "," + str(balanced)
			client_socket.send(bluetooth_message)
			print(bluetooth_message)
				
		reps_needed = 0
	
	
	
client_socket.close()
server_socket.close()		
		
		
