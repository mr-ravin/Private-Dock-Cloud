# Client Socket module

import socket as so

class ClientSocket:
	sockobj = None
	serverAddress = ('192.168.122.194',50007)
	#serverAddress = ('localhost',50007)
	
	def __init__(self):
		self.sockobj = so.socket(so.AF_INET,so.SOCK_DGRAM, 0 )
		self.sockobj.settimeout(40)
		
	def sendData(self,op_code):
		status = '91'
		op_code = bytes(op_code,encoding = 'ascii')
		self.sockobj.sendto(op_code,self.serverAddress)
		try:
			status = self.sockobj.recv(1024)
		except Exception: 
			print('Timeout Occured !!!')
			return '95'
		status = status.decode(encoding = 'ascii')
		return status
		
	def operation(self,info):
		print(info)
		returncode = self.sendData(info)
		return returncode


