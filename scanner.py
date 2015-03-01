#!/usr/bin/python
# multiproc_test.py

from time import sleep
import subprocess, platform, time, socket, sys, os
import multiprocessing
from datetime import datetime

class scanner:

	# * * * * * * * * * * * * * * * *
	def __init__(self):

		osname = platform.system()


		if osname == "Windows":
			clear = lambda: os.system('cls') 
		elif osname == "Linux":
			clear = lambda: os.system('clear')
		else:
			clear = lambda: os.system('')
		
		clear()


		# Determine the IP Addresses and the ports we are going to scan
		# In the future, check what our DHCP settings are, and automatically set to scan entire current working subnet ;)
		iplist = []
		portlist = ['80']
		
		# Set a range for IP's - let's scan the 192.168.1.1/24 subnet
		iprange = range(90,92)
		for i in iprange:
			iplist.append("192.168.1."+str(i))
		del i, iprange # We don't need these anymore
				
		# Clear the screen
		clear()
		
		# Check what time the scan started
		t1 = datetime.now()
		
		# Set Jobs list
		jobs = []
		
		try:

				for ip in iplist: 
					process = multiprocessing.Process(target=self.scan,args=(ip, portlist))
					jobs.append(process)
				# End ip in iplist
		
				# Start the processes		
				for j in jobs:
					j.start()
			
				# Ensure all of the processes have finished
				for j in jobs:
					j.join()
		
		except KeyboardInterrupt:
		    #print "You pressed Ctrl+C"
		    sys.exit()
		
		# Checking the time again
		t2 = datetime.now()
		
		# Calculates the difference of time, to see how long it took to run the script
		total =  t2 - t1
		
		# Printing the information to screen
		print 'Scanning Completed in: ', total
	# * * * * * * * * * * * * * * * *
	# End Def init

	# The scan function
	def scan(self, ip, portlist):
		try:
			reportopen = ""
			reportclose = ""
			for port in portlist:
				port = int(port)
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(2)
				result = sock.connect_ex((ip, port))
				if result == 0:
					reportopen += "\tOpen Port "+format(port)+"\n"
				else:
					reportclose += "\tClosed Port "+format(port)+"\n"
				sock.close()
	
			if reportopen != "":
				print "~" * 60
				print "IP: " + str(ip)
				print reportopen
				del reportopen
				if reportclose != "":
					print reportclose
					del reportclose
			
			sleep(1)
			
		except KeyboardInterrupt:
		    #print "You pressed Ctrl+C"
		    sys.exit()

	# * * * * * * * * * * * * * * * *	
	# End Def scan



if __name__ == '__main__':
	multiprocessing.freeze_support()

#
# * * * * * * * * * * *
#                   # *
scanner = scanner() # * # Run the script!
#                   # *
# * * * * * * * * * * *
#


