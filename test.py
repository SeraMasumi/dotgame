import subprocess

def execute(cmd):
    popen = subprocess.Popen(cmd, shell=True, bufsize=1,stdout=subprocess.PIPE,universal_newlines=True)
   # try:
    #    outs, errs = popen.communicate(timeout=15)
    #    yield outs
    #except TimeoutExpired:
    #    popen.kill()
    #    outs, errs = popen.communicate()
    #    yield outs
    
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait(timeout=10)
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
      
for path in execute(["sudo ./ads1256_test"]): #ads1256_test
    print(path, end="")
