import serial
import string
import serial
class usbcid:
	def __init__(self, Port = 0, Timeout = None):
                self.ser = serial.Serial('COM25', 4800,timeout=1)
#                self.ser = serial.Serial('/dev/usb/tts/0', 1200,timeout=1)
		self.buf = ''
		

	def computetemp(self,hh,ll):
		print 'hh',hh
		print 'll',ll
		xtemp= hh*255+ll
		print "%02x " % xtemp;
		if xtemp > 0x4000:
			xdtemp=-(0x4000-(xtemp/4))*0.03125
		else:
			xdtemp=(xtemp/4)*0.03125
		return xdtemp
	def readtemp1(self):	
		hh=0;
		ll=0;
		count = 0 
		while 1:

				x= self.ser.read()
				print "%02x " % ord(x[0]);		
				if ord(x[0])==0x24:
					print 'find header'
					count =0;
				else:
					count=count+1;
					print count
				if count ==3:
					hh=ord(x[0])
					print hh
				if count ==4:
					ll=ord(x[0])
				if ord(x[0])==0x55:
					temp = self.computetemp(hh,ll)
					print 'temp='
					print temp
					
	def readtemp(self,bSend):		
		atstring = chr(0x24)+chr(0x10)+chr(0x05)+chr(0x01)+chr(0x1)+chr(0x00)+chr(0x32)+chr(0x01)+chr(0x55)
#		self.ser.write(0x24)
#		self.ser.write(0x10)
#		self.ser.write(0x05)
#		self.ser.write(0x01)
#		self.ser.write(0x01)
#		self.ser.write(0x00)
#		self.ser.write(0x32)
#		self.ser.write(0x01)
#		self.ser.write(0x55)
		if bSend:
			self.ser.write(atstring)
		hh=0;
		ll=0;
		count = 0 
		while 1:
				x= self.ser.read()
#				print len(x)
				if len(x)==0:
					return 0
				print "%02x " % ord(x[0]);
				if ord(x[0])==0x24:
					print 'find header'
					count =0;
				else:
					count=count+1;
				if count ==3:
					hh=ord(x[0])
				if count ==4:
					ll=ord(x[0])
				if ord(x[0])==0x55 and count==5:
					temp = self.computetemp(hh,ll)
					print 'temp='
					print temp
					return 1
					break;
	def closecom(self):
		self.ser.close()
						
ser = usbcid('COM25',Timeout=1)

iret = ser.readtemp(True)
if iret==0:
		iret = ser.readtemp(False)
ser.closecom()