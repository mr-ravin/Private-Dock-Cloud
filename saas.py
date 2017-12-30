#!/usr/bin/python

# SaaS

import _thread
import os
import subprocess

sip = "192.168.122.194"


def start(a):
	#commands.getstatus(a)
        subprocess.getstatusoutput(a)
	#os.system(a)
        
def call(uname,upass,choice):
	ch = None
	choice = choice.lower()
	if choice == 'gedit':
		ch = 'gedit'
	elif choice == 'browser' :
		ch = 'firefox'
	elif choice == 'python interpreter':
		ch = 'python'
	elif choice == 'libre office':
		ch = 'libreoffice4.3'
	elif choice == 'vncviewer':
		ch = 'vncviewer'
	
	a= "sshpass -p "+ upass +" ssh -X " + uname +"@"+ sip + "  " + ch
	_thread.start_new_thread(start,(a,))
	print (a)
	
