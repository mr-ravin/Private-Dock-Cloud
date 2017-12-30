import subprocess
import string
import random

def createspace(username):
    print(subprocess.getstatusoutput('lvcreate --name ' + username + '  --size 512M ' + '/dev/cloud'))
    print(subprocess.getstatusoutput('mkfs.ext4  /dev/cloud/'+username))
    print(subprocess.os.mkdir('/cloud/'+username))
    print(subprocess.getstatusoutput('systemctl restart nfs-server'))

def create_account(username):
    print('hello')
    status = subprocess.os.system('useradd --home-dir /cloud/'+username+'  '+ username)
    print('Bye')
    print(subprocess.getstatusoutput('mount /dev/cloud/' + username + '  /cloud/' + username))
    print(subprocess.getstatusoutput('echo \"/cloud/' + username + '  192.168.122.194/0.0.0.0(rw,no_root_squash)\" ' + '>> /etc/exports'))
    print(subprocess.getstatusoutput('systemctl restart nfs-server'))
    print(subprocess.getstatusoutput('chown '+username+' /cloud/' + username + ' -R'))
    if status == 0:
             return True
    else:
             return False

def random_text():
    text = ''
    for i in range(15):
        text += random.choice(string.hexdigits)
    return text
    
def change_password(username,key):
    a,b = subprocess.getstatusoutput('echo -e \"' + key + '\\n' + key + '\\n\"' + ' | passwd '+ username)
    if not a:
        return True
    else:
        return False

def lvreduce(value,username):
    print(subprocess.getstatusoutput('systemctl stop nfs-server'))
    print(subprocess.getstatusoutput('umount /cloud/'+username))
    print(subprocess.getstatusoutput('e2fsck -f  /dev/cloud/'+username))
    print(subprocess.getstatusoutput('resize2fs   /dev/cloud/'+username+ '  '+str(value)+'M'))
    print(subprocess.getstatusoutput('lvreduce -f --size '+str(value)+'M  /dev/cloud/'+username))
    print(subprocess.getstatusoutput('mount /dev/cloud/' + username + '  /cloud/' + username))
    print(subprocess.getstatusoutput('systemctl restart nfs-server'))

def lvextend(value,username):
    print(subprocess.getstatusoutput('lvextend --size '+str(value)+'M  /dev/cloud/'+username))
    print(subprocess.getstatusoutput('resize2fs   /dev/cloud/'+username))
        
