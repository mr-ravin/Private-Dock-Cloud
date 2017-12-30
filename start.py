from server import *
import _thread

class Console:
    serverobj = ServerSocket()
    def start(self):
        self.serverobj.startRecv()
    def stop(self):
        self.serverobj.stopRecv()

SERVER = Console()
SERVER.start()
#root = Tk()
#root.title('Server')
#Label(root,text='BestWorker Cloud Server',font='Times 20 bold',fg='#ff0099',justify=CENTER).pack(padx=10,pady=10,side=TOP,fill=X)
#Button(root,text='Start',command = start,width=20,height=3,bg='#ff1111',font='Times 15 bold italic',fg='#000099').pack(padx=10,pady=10,side=LEFT)
#Button(root,text='Stop',command = stop,width=20,height=3,bg='#ff0011',font='Times 15 bold italic',fg='#000099').pack(padx=10,pady=10,side=LEFT)
#root.mainloop()
