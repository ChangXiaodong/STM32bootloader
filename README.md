# STM32bootloader
This repository is a re-distribution of Ivan's project (Project page: http://tuxotronic.org/wiki/projects/stm32loader) and reedit from changtengfei by changxiaodong 

#Hardware setup

In the original version, using this script need to corporate with the set and reset on BOOT0 and RESET pin. The set and reset usually were executed by hand. To create a totally automatic download process, you need to modified your hardware stm32 devices. Following are the steps you need to follow:
1.Identify you UART-to-USB Chip you are using and find the RTS and DTR pin. 
2.Connect the RTS pin on your UART-to-USB Chip to the BOOT0 pin on you STM32 device
3.Connect the DTR pin on your UART-to-USB Chip to the RESET pin on you STM32 device


Note: For the connection of pins in steps 2 and 3, you can change the order in an opposite way(RTS->RESET, DTR->BOOT0). If you do this, you need exchange the usage of setRTS() and setDTR() functions in bootloader.py. 

#STM32Loader

Python script which will talk to the STM32 bootloader to upload and download firmware.

#Usage: 
	   ./bin.py [-p program] [-l list] [-h help]
       ./run.py [-A All]Start all nodes [-l list]list exist ports [port num]
	   ./kill.py [-A All]Start all nodes [-l list]list exist ports [port num]

#Example: 
		 bin.py -p somefile.bin
		 This will pre-erase flash, write somefile.bin to the flash on the device, and then perform a verification after writing is finished.
         run.py -A 
		 start all nodes
		 run.py	-l 
		 list all ports
		 run.py	5-20 
		 start COM5 to COM20
		 run.py	5-20 15 16 17 
		 start COM5 to COM20 except COM15,COM16,COM17
		 run.py 14 18 19 
		 start COM14,COM18,COM19
		 kill.py is to stop running.
		 usage of kill.py is same to run.py
