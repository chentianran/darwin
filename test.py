import re
import subprocess
import os


p = subprocess.check_output(['/home/ovenhouse/h3/h3', 
	   				  '/home/ovenhouse/h3/testcases/barry.lee'], 
				      #stdout = subprocess.PIPE, 
					  stderr = subprocess.STDOUT)

#output = p.communicate()


pos = re.search('^Preprocess:\s*([0-9]+\.?[0-9]*)', p, flags=re.MULTILINE)
if( pos != None ):
	print pos.group(1)

	
