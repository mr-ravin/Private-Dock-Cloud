from socket import *
import subprocess as sub
import signal as sig
import _thread
import operations

def stop(signum,stackframe):
    global sockobj

    print('Shutting down the server.......')
    sockobj.close()
    exit()

sig.signal(sig.SIGINT, stop)


class ServerSocket:
    myhost = '192.168.122.194'
    myport = 50007
    sockobj = None
    
    def __init__(self):
        self.sockobj = socket(AF_INET, SOCK_DGRAM , 0 )
        self.sockobj.bind ((ServerSocket.myhost,ServerSocket.myport))

    def startRecv(self):
            print('Starting the server .....')
            while True:
                data = None
                address = None
                try:
                    data,address = self.sockobj.recvfrom(1024)
                except Exception:
                    print('Socket closed')
                    return
                data = data.decode(encoding = 'ascii')
                _thread.start_new_thread(self.action,(data,address))

    def action(self,commd,address):  #  performing the action requested by the client
        print(commd)
        code =  commd.split('/') 
        if code[0] == '01':
            reg_info = commd.lstrip('01/')
            status_code = self.registration(reg_info)
            self.sockobj.sendto(status_code.encode(encoding='ascii'), address)
            return
        elif code[0] == '02':
            log_details = commd.lstrip('02/')
            status_code = self.login_check(log_details)
            self.sockobj.sendto(status_code.encode(encoding='ascii'), address)
            return
        elif code[0] == '03':
            storage_data = commd.lstrip('03/')
            status_code = self.setvolume(storage_data)
            self.sockobj.sendto(status_code.encode(encoding='ascii'), address)
            return
        elif code[0] == '04':
            uname = commd.lstrip('04/')
            status_code = self.logout(uname)
            self.sockobj.sendto(status_code.encode(encoding='ascii'), address)
            return
            

    def stopRecv(self):
        print('Shutting down the server ...')
        self.sockobj.settimeout(1)
        #self.sockobj.close()

    def registration(self,reg_info):
        print(reg_info)
        info = reg_info.split('/')
        file = open('accounts.txt','r')
        accounts = file.read().split('\n')
        file.close()
        del accounts[-1]
        for acc in accounts:
            details = acc.split('/')
            if details[0] == info[0]:
                return '91'
            elif details[4] == info[4]:
                return '92'
            elif details[5] == info[5]:
                return '93'
        operations.createspace(info[0])
        flag = operations.create_account(info[0])
        if flag:
            file = open('accounts.txt','a')
            file.write(reg_info+'\n')
            file.close()
            return '00'
        else:
            return '94'
    
        

    def login_check(self,log_details):
        username,password = log_details.split('/')
        file = open('accounts.txt','r')
        accounts = file.read().split('\n')
        file.close()
        del accounts[-1]
        for acc in accounts:
            details = acc.split('/')
            if details[0] == username and details[1] == password:
                print('match found')
                key = operations.random_text()
                if operations.change_password(username,key):
                    return '00/'+ key
        else:
            return '91'

    def logout(self,uname):
        key = operations.random_text()
        if operations.change_password(uname,key):
            return '00'
        else:
            return '91'
            

    def setvolume(self,storage_data):
        data = storage_data.split('/')
        if data[3] == '01':
            operations.lvreduce(int(data[2]),data[0])
        else:
            operations.lvextend(int(data[2]),data[0])
        return '00'



        
#if __name__ == '__main__':

 #    serverobj = ServerSocket()  
