# GUI for the app
from client import *
from tkinter import *
import subprocess
import hashlib
import saas


class Application:
    username = ''
    password = ''
    key = None
    capacity = None
    directory = ''
    mounted = False
    left_frame = None
    displays = list()
    acc_frames = {}
    services = [ ("Account",0),("Softwares",1),("Storage",2),("Operating System",3)]
    #                  ,("Disks",3),("Instances",4) ]
    socket = None
    
    def __init__(self,master):
        global x,x_prev

        ###################################################
        ##Creating the client socket
        self.socket = ClientSocket()

        ##############################################
        # Creating the left Tab frame
        self.left_frame = Frame(master)
        self.left_frame.grid(row=1,column=0,sticky=W)
        

        #########################################################################
        # displays --- list of frames for each right window for a particular tab
        for index in range(5):
            self.displays.append( Frame(master,width=100,height=25) )
            

            
        ######################################################
        #selecting  account display window as default window 
        self.displays[0].grid(row=1,column=1,sticky=W)

        

        ##############################################
        # Adding the RadioButtons to the left Tab frame 
        
        for txt,val in self.services:
            Radiobutton(self.left_frame,
                        text=txt,
                        indicatoron = 0,
                        bg = "light green",
                        width = 30,
                        height= 5,
                        variable=x,
                        command=self.unmap,             # self.ShowChoice,
                        value=val).pack(anchor=W,side=TOP,fill=BOTH)


        ###################################
        #  Account information and login frame
        self.acc_frames['first'] = Frame(self.displays[0],width=100,height=25)
        self.acc_frames['login'] = Frame(self.displays[0],width=100,height=25)
        self.acc_frames['register'] = Frame(self.displays[0],width=100,height=25)
        self.setaccountframe()



        ####################################################################################################################
        #Softwares display frame
        self.soft_names = ['Gedit','Browser','Python Interpreter','Libre Office','VNCViewer']
        Label(self.displays[1],text='ALL AVAILABLE SOFTWARES',fg="#991111").grid(row=0,column=0,columnspan=2,pady=10)
        self.laun = IntVar()
        #self.laun.set(4)
        for name in self.soft_names:
            tmp = self.soft_names.index(name) + 1
            Label(self.displays[1],text= str(tmp) + '. ' + name,width=30,height=3,justify=LEFT,font="Times 11 bold").grid(row=tmp,column=0,sticky=W)
            Radiobutton(self.displays[1],text="Launch !!",width=30,height=3,command=self.launch,indicatoron = 0,state = 'active' ,value=self.soft_names.index(name),variable=self.laun).grid(row=tmp,column=1)



        #####################################################################################################################
        # Frame for the storage
        Label(self.displays[2],text='Storage and files',font="Times 16 bold").pack(fill=X,side=TOP)
        self.cap_size = Scale(self.displays[2],from_ = 512,to=4096,tickinterval=512,orient=HORIZONTAL,length=400,   \
                              activebackground='#234567',label='Select the storage space in MBs',resolution=512)
        self.cap_size.pack(padx=15,pady=10)
        self.capacity = self.cap_size.get()
        Button(self.displays[2],text='Set',command = self.setvolume,font="Times 11 bold").pack(padx=15,pady=10,fill=X)
        Button(self.displays[2],text='Mount',command = self.mount,font="Times 11 bold").pack(padx=15,pady=10,fill=X)
        Button(self.displays[2],text='Unmount',command = self.unmount,font="Times 11 bold").pack(padx=15,pady=10,fill=X)
        

        

    def launch(self):
        launch_choice = self.laun.get()
        saas.call(uname = self.username,upass = self.key, choice = self.soft_names[launch_choice])
    

    def unmap(self):
        if self.username == '':
            x.set(0)
            return
        self.displays[ x_prev.get() ].grid_forget()
        self.displays[ x.get() ].grid(row=1,column=1,sticky=W)
        x_prev.set(x.get())

        
    def ShowChoice(self):
        
        if x.get() == 0:
            print ("Account details")
        elif x.get() == 1:
            print ("Available Software")
        elif x.get() == 2:
            print ("Object Storage")
        elif x.get() == 3:
            print ("Disks")
        elif x.get() == 4:
            print ("Instances")


    def setaccountframe(self):
        
        self.msg = Label(self.acc_frames['first'],text="Welcome to PrivateDock Cloud Services",fg="#879898",font="Times 16 bold")
        self.msg.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        self.description = Message(self.acc_frames['first'],text='''PrivateDock provides the cloud solutions in the form of SaaS, STaaS, and OSaaS''')
        #self.description.insert(END,'''We provides the cloud solutions''')
        self.description.grid(row=1,columnspan=2,sticky=N)
        #Login Button
        self.loginbutton = Button(self.acc_frames['first'],text="Log In",command=self.gotologin,width=20,font="Times 11 bold")
        self.loginbutton.grid(row=4,column=0,pady=10)
        #Register Button
        self.regbutton = Button(self.acc_frames['first'],text="Register",command=self.register,width=20,font="Times 11 bold")
        self.regbutton.grid(row=4,column=1,pady=10)
        self.acc_frames['first'].grid()

        
    def gotologin(self):
        self.acc_frames['first'].grid_forget()
        Label(self.acc_frames['login'],text="Welcome to PrivateDock Cloud Services",fg="#879898",font="Times 16 bold").grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        Label(self.acc_frames['login'],text="Username",width=10,font="Times 11 bold").grid(row=2,column=0)
        self.acc_name = Entry(self.acc_frames['login'],font="Times 11 italic")
        self.acc_name.insert(30,"Enter Username")
        self.acc_name.grid(row=2,column=1)
        Label(self.acc_frames['login'],text="Password",width=10,font="Times 11 bold").grid(row=3,column=0)
        self.passw = Entry(self.acc_frames['login'],show='*',font="Times 11 italic")
        self.passw.insert(30,"Enter Password")
        self.passw.grid(row=3,column=1)
        self.loginbtn = Button(self.acc_frames['login'],text="Log In",command=self.login,width=20,font="Times 11 bold")
        self.loginbtn.grid(row=4,column=0,pady=10)
        self.backbutton = Button(self.acc_frames['login'],text="Back",command=self.back,width=20,font="Times 11 bold")
        self.backbutton.grid(row=4,column=1,pady=10)
        self.acc_frames['login'].grid()

    def back(self):
        self.acc_frames['login'].grid_forget()
        self.acc_frames['register'].grid_forget()
        self.acc_frames['first'].grid()
        
    def login(self):
        username = self.acc_name.get()
        password = self.passw.get()
        if username.upper().strip() == 'ENTER USERNAME' or username.strip() == '' :
            messagebox.showinfo('Message','Fill the username field properly')
            return
        if password.upper() == 'ENTER PASSWORD' or password == '':
            messagebox.showinfo('Message','Fill the password field properly') 
            return

        
        ###########################################################################
        ## Performing the hashing
        password = Application.hashing(password)
        
        #############################################################################
        #perfoming verification of account details
        info = '02'
        info += '/' + username
        info += '/' + password
        #print(info)
        #if 1:
        returncode = self.socket.operation(info).split('/')
        if returncode[0] == '00':
            self.username = username
            self.password = password
            self.key = returncode[1]
            self.acc_name.grid_forget()
            self.passw.grid_forget()
            self.loginbtn.grid_forget()
            self.backbutton.grid_forget()
            Label(self.acc_frames['login'],text=self.username,width=20,height=5,font="Times 11 italic").grid(row=2,column=1)
            Label(self.acc_frames['login'],text='********',width=20,height=5,font="Times 11 italic").grid(row=3,column=1)
            self.logoutbtn = Button(self.acc_frames['login'],text='LogOut',width=20,command=self.logout,font="Times 11 bold")
            self.logoutbtn.grid(row=4,columnspan=2,pady=10)
            return
        elif returncode[0] == '91':
            #messagebox.showerror('Login failed','Incorrect username or password !!! ')
            print('Login failed','Incorrect username or password !!! ')
            return

    def logout(self):
        info = '04'
        info += '/' + self.username
        status =self.socket.operation(info)
        self.username = ''
        self.password = ''
        self.key = ''
        if status == '00':
            #messagebox.showinfo('Logout','Successfully Logged out !!!')
            print('Logout','Successfully Logged out !!!')
            self.logoutbtn.grid_forget()
            self.acc_frames['login'].grid_forget()
            self.acc_frames['first'].grid()
        else:
            #messagebox.showinfo('Alert','Some unusual happened !!!')
            print('Alert','Some unusual happened !!!')
            self.destroy()

        
    def register(self):
        self.acc_frames['first'].grid_forget()
        Label(self.acc_frames['register'],text="Welcome to PrivateDock Cloud Services",fg="#879898",font="Times 16 bold").grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        Label(self.acc_frames['register'],text='Username',width=20,height=2,font="Times 11 bold").grid(row=1,column=0)
        self.uname = Entry(self.acc_frames['register'],font="Times 11 italic")
        self.uname.insert(30,"Enter username")
        self.uname.grid(row=1,column=1)
        Label(self.acc_frames['register'],text='First Name',width=20,height=2,font="Times 11 bold").grid(row=2,column=0)
        self.first_name = Entry(self.acc_frames['register'],font="Times 11 italic")
        self.first_name.insert(30,"Your First Name")
        self.first_name.grid(row=2,column=1)
        Label(self.acc_frames['register'],text='Last Name',width=20,height=2,font="Times 11 bold").grid(row=3,column=0)
        self.last_name = Entry(self.acc_frames['register'],font="Times 11 italic")
        self.last_name.insert(30,"Your Last Name")
        self.last_name.grid(row=3,column=1)
        Label(self.acc_frames['register'],text='Password',width=20,height=2,font="Times 11 bold").grid(row=4,column=0)
        self.rpassword = Entry(self.acc_frames['register'],show='*',font="Times 11 italic")
        self.rpassword.insert(30,"Enter Password")
        self.rpassword.grid(row=4,column=1)
        Label(self.acc_frames['register'],text='Confirm Password',width=20,height=2,font="Times 11 bold").grid(row=5,column=0)
        self.rcpassword = Entry(self.acc_frames['register'],show='*',font="Times 11 italic")
        self.rcpassword.insert(30,"ENTER PASSWORD")
        self.rcpassword.grid(row=5,column=1)
        Label(self.acc_frames['register'],text='Mobile Number',width=20,height=2,font="Times 11 bold").grid(row=6,column=0)
        self.phone = Entry(self.acc_frames['register'],font="Times 11 italic")
        self.phone.insert(30,"Enter contact number")
        self.phone.grid(row=6,column=1)
        Label(self.acc_frames['register'],text='Email',width=20,height=2,font="Times 11 bold").grid(row=7,column=0)
        self.email = Entry(self.acc_frames['register'],font="Times 11 italic")
        self.email.insert(30,"Enter email")
        self.email.grid(row=7,column=1)
        Button(self.acc_frames['register'],text="Register",width=20,command=self.validate,font="Times 11 bold").grid(row=8,column=0,padx=10,pady=10)
        Button(self.acc_frames['register'],text="Back",command=self.back,width=20,font="Times 11 bold").grid(row=8,column=1,padx=10,pady=10)
        self.acc_frames['register'].grid()

    def validate(self):

        if self.uname.get().strip() == "Enter username" or self.uname.get().strip() == '':
            #messagebox.showinfo('Error','Fill the username field !!!')
            print('Error','Fill the username field !!!')
            return
        elif not self.uname.get().isalnum():
            #messagebox.showinfo('Error','Only Alphanumeric characters are allowed !!!')
            print('Error','Only Alphanumeric characters are allowed !!!')
            return
        
        if self.first_name.get().strip() == 'Your First Name' or self.first_name.get().strip() == '':
            #messagebox.showinfo('Error','Fill the first name field !!!')
            print('Error','Fill the first name field !!!')
            return
        elif not self.first_name.get().strip().isalpha() :
            #messagebox.showinfo('Error','First name can contain only alphabets !!!')
            print('Error','First name can contain only alphabets !!!')
            return
        
        if self.last_name.get().strip() == 'Your Last Name' or self.last_name.get().strip() == '' :
            #messagebox.showinfo('Error','Fill the last name field !!!')
            print('Error','Fill the last name field !!!')
            return
        elif not self.last_name.get().strip().isalpha() :
            #messagebox.showinfo('Error','Last name can contain only alphabets !!!')
            print('Error','Last name can contain only alphabets !!!')
            return

        if self.phone.get().strip() == "Enter contact number" or self.phone.get().strip() == "":
            #messagebox.showinfo('Error','Fill the Mobile number field !!!')
            print('Error','Fill the Mobile number field !!!')
            return
        elif not self.phone.get().lstrip('+').isdigit() :
            #messagebox.showinfo('Error','Only numeric values allowed !!!')
            print('Error','Only numeric values allowed !!!')
            return
        elif len(self.phone.get().lstrip('+')) != 10 and len(self.phone.get().lstrip('+')) != 12  :
            messagebox.showinfo('Error','Invalid Mobile number !!!')
            print('Error','Invalid Mobile number !!!')
            return

        if self.email.get() == "Enter email" or self.email.get() == "" :
            #messagebox.showinfo('Error','Fill the email field !!!')
            print('Error','Fill the email field !!!')
            return
        elif self.email.get().find('@') == -1 or self.email.get().find(' ') != -1 : 
            #messagebox.showinfo('Error','Invalid email address!!!')
            print('Error','Invalid email address!!!')
            return
        
        self.regClient() 
                                                                                     
    def regClient(self):
        
        if self.rpassword.get() != self.rcpassword.get():
            #messagebox.showerror('Error','Passwords are not matching')
            print('Error','Passwords are not matching')
            return

        ###############################
        ## hashing the password with sha512
        passwd = Application.hashing(self.rpassword.get())
        
        info = '01'
        info += '/' + self.uname.get()
        info += '/' + passwd
        info += '/' + self.first_name.get()
        info += '/' + self.last_name.get()
        info += '/' + self.phone.get()
        info += '/' + self.email.get()
        #print(info)
        #return
        status = self.socket.operation(info)
	
        if status == '00':
            #messagebox.showinfo('Registration','Successfully registered !!! \n\n Login to use services \n\n')
            print('Registration','Successfully registered !!! \n\n Login to use services \n\n')
            self.acc_frames['register'].grid_forget()
            self.acc_frames['first'].grid()
            return
        elif status == '91':
            #messagebox.showinfo('Registration','The given username already exists !!!')
            print('The given username already exists !!!')
            return
        elif status == '92':
            #messagebox.showinfo('Registration','Phone Number is already registered !!!')
            print('Phone Number is already registered !!!')
            return
        elif status == '93':
            #messagebox.showinfo('Registration','Given Email address is already registered !!!')
            print('Given Email address is already registered !!!')
            return
        else:
            #messagebox.showinfo('Registration','There is some technical problem. Please contact the administrator !!!')
            print('There is some technical problem. Please contact the administrator !!!')
            return
 

    def setvolume(self):
        capacity = self.cap_size.get()
        if capacity == self.capacity:
            #messagebox.showinfo('Information','First change the size of volume !!!')
            print('Information','First change the size of volume !!!')
            return
        elif capacity < self.capacity and self.mounted == True:
            #messagebox.showinfo('Information','First unmount the storage space !!!')
            print('First unmount the storage space !!!')
            return
        
        info = '03'
        info += '/' + self.username
        info += '/' + self.password
        info += '/' + str(capacity)
        if capacity < self.capacity:
            info += '/' + '01'
        else:
            info += '/' + '02'
        status = self.socket.operation(info)
        if status == '00':
            self.capacity = capacity
            #messagebox.showinfo('Operation successful','The Capacity has been set to '+str(capacity)+' MBs !!')
            print('Operation successful','The Capacity has been set to '+str(capacity)+' MBs !!')
            return
        elif status == '91':
            #messagebox.showerror('Operation failed','Unable to complete the request \n\n Make sure you are connected to the network \n else contact the administrator !!')
            print('Operation failed','Unable to complete the request \n\n Make sure you are connected to the network \n else contact the administrator !!')
            return

    
    def mount(self):
        if self.mounted == True:
            print('Storage space is already mounted !!!')
            return
        #self.directory = subprocess.os.getenv('HOME')
        self.directory = subprocess.getoutput('cd ; pwd') +  '/' + 'PrivateDock'
        status = subprocess.os.path.isdir( self.directory)
        if status == False:
            subprocess.os.mkdir(self.directory)
            
        subprocess.getstatusoutput('mount  ' + saas.sip + ':/cloud/' + self.username + \
                                   '    ' + self.directory)
        self.mounted = True
        print('Mount successful !!! \n\n  At '+ self.directory )

    def unmount(self):
        if self.mounted == False:
            print('Storage space is not mounted !!!')
            return
        a,b = subprocess.getstatusoutput ('umount ' + self.directory)
        if not a: 
            print('Umount successful !!!')
            self.mounted = False
        
    @staticmethod
    def hashing(value):
        return hashlib.sha512(value.encode(encoding='ascii')).hexdigest()



root = Tk()
root.title('PrivateDock')
x = IntVar()
x_prev = IntVar()
x.set(0)
x_prev.set(x.get())
app = Application(root)
root.mainloop()
