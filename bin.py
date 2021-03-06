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

	chip_ids = {
		0x412: "STM32 Low-density",
		0x410: "STM32 Medium-density",
		0x414: "STM32 High-density",
		0x420: "STM32 Medium-density value line",
		0x428: "STM32 High-density value line",
		0x430: "STM32 XL-density",
		0x416: "STM32 Medium-density ultralow power	line",
		0x411: "STM32F2xx",
		0x413: "STM32F4xx",
	}
	
	def	__init__(self,port,baund = 115200, address = 0x08000000):
		self.port	 = port
		self.baund	 = baund
		self.address = address
		self.cmd	 = CommandInterface()
	
	def	initialChip(self):

		self.cmd.open(self.port, self.baund)
		print "Open	port" +	self.port +	", baud	" +	str(self.baund)
		self.cmd.initChip()

	# turn of debugging	information
	def	turnOffDebugging(self):
		self.cmd.quiet()
	
	# this function	will download the target file to the device	at 0x8000000 and verify.
	def	downloadJob(self,binFile):
		status = False # True instead of success, False	instead	of Failed
		print "1. Erase	memory first. Erasing..."
		self.cmd.cmdEraseMemory(WRPxPages)
		print "2. Erase	Done. Waiting for writing..."
		data = map(lambda c: ord(c), file(binFile, 'rb').read())
		self.cmd.writeMemory(self.address, data)
		print "3. EndOfWrite. Waiting for verifying..."
		verify = self.cmd.readMemory(self.address, len(data))
		if(data	== verify):
			print "4. Verification OK"
			print "Download	on port	" +	self.port +	" successfully!	:)"
			status = True
		else:
			print "4. Verification FAILED"
			print str(len(data)) + ' vs	' +	str(len(verify))
			for	i in xrange(0, len(data)):
				if data[i] != verify[i]:
					print hex(i) + ': '	+ hex(data[i]) + ' vs '	+ hex(verify[i])
		return status
		
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
	
	serialPort = "COM6"
	portlistsort = []
	# get options and arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:], "p:lh")
	except getopt.GetoptError, err:
		# print	help information and exit:
		print str(err) # will print	something like "option -a not recognized"
		sys.exit(2)
	
	# filter options
	for	option,value in	opts:
		if option == '-p':
			serialPort = str(value)
		elif option	== '-h':
			print ""
			print "Usage: bin [-p] [-l]	[-h] "
			print "Parameters:"
			print "	   -p: example:'reset -p COM5 led_toggle.bin'"
			print "	   -l: list	all	serial ports"
			print "	   -h: for help"
			sys.exit(0)

		elif option	== '-l':
			portlist = SerialPorts()
			portlist.enumerate_serial_ports()
			for	portnum	in range(len(portlist.portList)):
				portlistsort.append(str(portlist.portList[portnum][1]))
			portlistsort=sorted(portlistsort)
			for	portname in	portlistsort:
				print portname
			exit(0)
		else:
			assert False, "can't handled the option"
			sys.exit(2)
		
	# create an	bootloader jobs	object
	bljobs = BootLoaderJobs(serialPort)
	bljobs.initialChip()
	bljobs.downloadJob(args[0])
	bljobs.killport()
			
	

