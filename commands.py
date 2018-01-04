from subprocess import *

def get_status_output(cmd,input=None,cwd=None,env=None):
	pipe = Popen(cmd,shell = True, cwd = cwd, env=env,stdout = PIPE, stderr = STDOUT)
	(output,errout) = pipe.communicate(input=input)
	assert not errout
	status = pipe.returncode
	return (status,output)
	
def get_status_output_errors(cmd,input=None,cwd=None,env=None):
	pipe = Popen(cmd,shell = True, cwd = cwd, env=env,stdout = PIPE, stderr = PIPE)
	(output,errout) = pipe.communicate(input=input)
	assert not errout
	status = pipe.returncode
	return (status,output,errout)	

def get_output(cmd):
	return get_status_output(cmd)[1]
	