import os
import re
import subprocess


out = subprocess.check_output(['/home/ovenhouse/h3/h3', '/home/ovenhouse/h3/testcases/barry.lee'])

lines = out.splitlines()

for line in lines:
	pos = re.search('^Failed:\s*([0-9]+)', line, flags=re.MULTILINE)
	if( pos != None ):
		print pos.group(0)
	
