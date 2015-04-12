# This file	is part	of stm32loader.
#
# stm32loader is free software;	you	can	redistribute it	and/or modify it under
# the terms	of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or	(at	your option) any later
# version.
#
# stm32loader is distributed in	the	hope that it will be useful, but WITHOUT ANY
# WARRANTY;	without	even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A	PARTICULAR PURPOSE.	 See the GNU General Public	License
# for more details.
#
# You should have received a copy of the GNU General Public	License
# along	with stm32loader; see the file COPYING3.  If not see
# <http://www.gnu.org/licenses/>.

import sys,	getopt
from bootloader	import CommandInterface
from serialport	import SerialPorts

# the pages	that contains the code,	pages 62~255 are protected by storing the 64 bits address.
# before downloading the code, pages 0~61 should be	erased first.
WRPxPages  = [i	for	i in range(	0, 62)]

class BootLoaderJobs():
	
	def	__init__(self,port,baund = 115200, address = 0x08000000):
		self.port	 = port
		self.baund	 = baund
		self.address = address
		self.cmd	 = CommandInterface()
	
	def	initialChip(self):

		self.cmd.open(self.port, self.baund)
		print "Run " + self.port
		self.cmd.initChip()

	def	getChipInformation(self):
		bootversion	= self.cmd.cmdGet()
		print "Bootloader version "	+ str(bootversion)
		chipId = self.cmd.cmdGetID()
		print "Chip	id:	0x"	+ str(chipId) +	" "	+ self.chip_ids.get(chipId,	"Unknown")
		
	def	releasePort(self):
		self.cmd.releaseChip()
		self.cmd.sp.close()
	def killport(self):
		self.cmd.killChip()
		self.cmd.sp.close()
	

if __name__	== "__main__":
	
	serialPort = []
	ExpserialPort = []
	portlistsort = []
	# get options and arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:], "Al")
	except getopt.GetoptError, err:
		# print	help information and exit:
		print str(err)	# will print something like	"option	-a not recognized"
		sys.exit(2)
	portlist = SerialPorts()
	portlist.enumerate_serial_ports()
	for portnum in range(len(portlist.portList)):
		portlistsort.append(str(portlist.portList[portnum][1]))
	portlistsort=sorted(portlistsort)
	if(len(args)>0):
		getport = str(args[0])
		if '-' in getport:
			ad = getport.split('-')
			StartNum = int(ad[0]);
			EndNum = int(ad[1]);
			for PortNum in range(StartNum,EndNum+1):
				serialPort.append(PortNum)
		else:
			for ports in args:
				serialPort.append(ports)
		if(len(args)>1):
			for ports in args[1:]:
				ExpserialPort.append(int(ports))
	if(len(opts)>0):
		for	option,value in opts:
			if option == '-A':
				for portnum in range(len(portlist.portList)):
					bljobs = BootLoaderJobs(portlist.portList[portnum][1])
					bljobs.initialChip()
					bljobs.releasePort()
				exit(0)
			elif option	== '-l':
				for portname in portlistsort:
					print portname
				exit(0)
#			elif option	== '-h':
#				print ""
#				print "Usage: reset	[NULL] [-p]	[-l] [-h] "
#				print "Parameters:"
#				print "	   NULL: reset all serial ports"
#				print "	   -p: reset a selected	port example:'reset	-p COM5' for reset COM5"
#				print "	   -l: list	all	serial ports"
#				print "	   -h: for help"
#				sys.exit(0)
#			else:
#				assert False, "can't handled the option"
#				sys.exit(2)
	for killpornum in serialPort:
		if killpornum in ExpserialPort:
			pass
		else:
			if ('COM'+str(killpornum)) not in portlistsort:
				print "port isn't exist"
			else:
				bljobs = BootLoaderJobs('COM'+str(killpornum))
				bljobs.initialChip() 
				bljobs.releasePort()


	

