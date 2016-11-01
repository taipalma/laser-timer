import threading
import sys
import usb.core
import usb.util

class USBthread(threading.Thread):
    def __init__(self, ui):
        
        threading.Thread.__init__(self)
        
        print "Initializing USB thread..."
        self.ui = ui

        # Initialize USB

        # hexidecimal vendor and product values, can be obtained with "lsusb -v" command in terminal
        self.__dev = usb.core.find(idVendor=0x04fc, idProduct=0x0801)
        
        # first endpoint
        self.__interface = 0
        self.__endpoint = self.__dev[0][(0,0)][0]

        # if the OS kernel already claimed the device, which is most likely true
        if self.__dev.is_kernel_driver_active(self.__interface) is True:
            # tell the kernel to detach
            self.__dev.detach_kernel_driver(self.__interface)
            # claim the device
            usb.util.claim_interface(self.__dev, self.__interface)
        
	
    def run(self):

        print "Running..."
        
        while self.ui.isTerminated() == False:
            try:
                data = self.__dev.read(self.__endpoint.bEndpointAddress, self.__endpoint.wMaxPacketSize)
                # if laser goes off, stop the timer
                if data[0] == 1:
                    self.ui.usbStop()
                
            except usb.core.USBError as e:
                data = None
                if e.args == ('Operation timed out',):
                    continue
        
        # release the device
        usb.util.release_interface(self.__dev, self.__interface)
        # reattach the device to the OS kernel
        self.__dev.attach_kernel_driver(self.__interface)
        
        print "USB released."
        
	    



