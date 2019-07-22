# Parsing data from HPSA zip files and outputing to CSV file

import zipfile, csv, re, os

def write_to_csv():
	csv_file = "output.csv"

	csv = open(csv_file, "w")

	TitleRow = "Number;Hostname;IP address;Interface;Destination;Gateway\n"
	csv.write(TitleRow)

	aix_data = get_aix_data()
	linux_data = get_linux_data()
	windows_data = get_windows_data()

	csv_data = []
	
	for data in aix_data:
		csv_data.append(data)
		
	for data in linux_data:
		csv_data.append(data)
		
	for data in windows_data:
		csv_data.append(data)
		
	for idx, line in enumerate(csv_data):
		csv_data[idx] = [str(idx+1)] + line
		
	for data in csv_data:
		row = data[0] + ";" + data[1] + ";" + data[2] + ";" + data[3] + ";" + data[4] + ";" + data[5] + "\n"
		csv.write(row)
	
	if os.path.isfile('./output.csv'):
		print("output.csv was successfully generated in path", os.path.abspath(os.path.dirname('./output.csv')))
	else:
		print("output failed")
		
def get_windows_data():

	WindowsZip = zipfile.ZipFile('Windows.zip', 'r')
	
	stdouts = []
	for file in WindowsZip.namelist():
		if file.endswith('stdout.txt'):
			stdouts.append(file)
	stdouts.sort()
	
	windows = []
	
	for stdout in stdouts:
			
		host = stdout.split(".")
		hostname = host[0]
		
		stdout_data = WindowsZip.read(stdout)
		all_lines = stdout_data.decode("utf-8", 'ignore')
		lines = all_lines.split("\n")
		
		routes = []
		ips = []
		interfaces = []
		windows_data = []
		entries = [None]*5
		
		if not all_lines:
			entries[0] = hostname
			entries[1] = 'no data'
			entries[2] = 'no data'
			entries[3] = 'no data'
			entries[4] = 'no data' 
			windows_data.append(entries)
			entries=[None]*5
		
		for line in lines:  
			if not line == 'Persistent Routes:':
				if "10.74" in line:
					routes.append(line)
			else:
				break
				
		for idx, line in enumerate(routes):
			routes[idx] = line.split()
			
		for line in lines:
			if 'Ethernet adapter' in line:
				rp = line.replace(":", " ")
				rp = rp.split()
				interfaces.append(rp[2])
			if 'IPv4 Address' in line:
				rp = re.sub("\(Preferred\)", '', line)
				rp = re.sub(" ", '', rp)
				rp = rp.split(":")
				ips.append(rp[1])
				
		ins = dict(zip(ips, interfaces))
		
		for route in routes:						
			entries[0] = hostname
			entries[1] = route[3]
			entries[2] = ins[route[3]]
			entries[3] = route[0]
			entries[4] = route[2]

			windows_data.append(entries)
			entries=[None]*5
			
		interfaces = []
		for route in windows_data:
			interfaces.append(route[2])

		for key in ins:
			if ins[key] not in interfaces:
				entries[0] = hostname
				entries[1] = key
				entries[2] = ins[key]
				entries[3] = 'no route'
				entries[4] = 'no route'	
				windows_data.append(entries)
				interfaces.append(ins[key])
				entries=[None]*5
				
		windows_data.sort(key=lambda x: x[2])
		
		for route in windows_data:
			windows.append(route)

	WindowsZip.close()
	
	return windows
	
def get_aix_data():
	
	AixZip = zipfile.ZipFile('AIX.zip', 'r')

	stdouts = []
	for file in AixZip.namelist():
		if file.endswith('stdout.txt'):
			stdouts.append(file)
	stdouts.sort()
	
	aix = []
	
	for stdout in stdouts:
	
		stdout_data = AixZip.read(stdout)
		all_lines = stdout_data.decode("utf-8")
		lines = all_lines.split("\n")
		
		if "/" in stdout:
			host = stdout.split("/")
		else:
			host = stdout.split("\\")
		hostname = host[0]

		ips = []
		entries = [None]*5
		aix_data = []
		interfaces = []
		routes = []

		if not all_lines:
			entries[0] = hostname
			entries[1] = 'no data'
			entries[2] = 'no data'
			entries[3] = 'no data'
			entries[4] = 'no data' 
			aix_data.append(entries)
			entries=[None]*5

		for line in lines:  
			if not line == 'Routing tables':
				if "10.74" in line:
					ips.append(line)
			else:
				break
		
		for idx, line in enumerate(ips):
			ips[idx] = line.split()
			interfaces.append(ips[idx][0])

		rt = False
		for line in lines:
			if line == 'Routing tables':
				rt = True
			if rt:
				for interface in interfaces:
					if interface in line:
						routes.append(line)
		
		for idx, route in enumerate(routes):
			routes[idx] = route.split()
			
		for route in routes:
			inet = ''
			for ip in ips:
				if route[5] == ip[0]:
					inet = ip[3]

			entries[0] = hostname
			entries[1] = inet
			entries[2] = route[5]
			
			if route[0] == 'default':
				entries[3] = '0.0.0.0'
			else:
				entries[3] = route[0]

			entries[4] = route[1]
			aix_data.append(entries)
			entries=[None]*5
		
		interfaces = []
		for route in aix_data:
			interfaces.append(route[2])

		for inet in ips:
			if inet[0] not in interfaces:
				entries[0] = hostname
				entries[1] = inet[3]
				entries[2] = inet[0]
				entries[3] = 'no route'
				entries[4] = 'no route'
				aix_data.append(entries)
				interfaces.append(inet[0])
				entries=[None]*5
		
		aix_data.sort(key=lambda x: x[2])

		for route in aix_data:
			aix.append(route)
			
	AixZip.close()
	
	return aix

def get_linux_data():

	LinuxZip = zipfile.ZipFile('Linux.zip', 'r')

	stdouts = []
	for file in LinuxZip.namelist():
		if file.endswith('stdout.txt'):
			stdouts.append(file)
	stdouts.sort()

	linux = []
	
	for stdout in stdouts:

		host = stdout.split(".")
		hostname = host[0]

		stdout_data = LinuxZip.read(stdout)
		all_lines = stdout_data.decode("utf-8")
		lines = all_lines.split("\n")

		ips = []
		routes = []
		entries = [None]*5
		linux_data = []
		interfaces = []
		
		if not all_lines:
			entries[0] = hostname
			entries[1] = 'no data'
			entries[2] = 'no data'
			entries[3] = 'no data'
			entries[4] = 'no data' 
			linux_data.append(entries)
			entries=[None]*5

		for line in lines:
			if 'inet' in line:
				ips.append(line)

		for line in lines:
			if 'via' in line:
				routes.append(line)

		for idx, line in enumerate(ips):
			ips[idx]=line.split(' ')

		for line in routes:
			line=line.split(' ')
			ip=''
			for inet in ips:
				if len(inet) == 11 and line[4] == inet[10]:
					ip = inet[5]
			
			entries[0] = hostname
			entries[1] = ip
			entries[2] = line[4]

			if line[0] == 'default':
				entries[3] = '0.0.0.0'
			else:
				entries[3] = line[0]

			entries[4] = line[2]

			linux_data.append(entries)
			entries=[None]*5

		for route in linux_data:
			interfaces.append(route[2])

		for inet in ips:
			if len(inet) == 11:
				if inet[10] not in interfaces:
					entries[0] = hostname
					entries[1] = inet[5]
					entries[2] = inet[10]
					entries[3] = 'no route'
					entries[4] = 'no route'
					linux_data.append(entries)
					interfaces.append(inet[10])
					entries=[None]*5
		
		linux_data.sort(key=lambda x: x[2])

		for route in linux_data:
			linux.append(route)

	LinuxZip.close()
	
	return linux

write_to_csv()