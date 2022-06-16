# Import the required libraries
import psutil
import time
from subprocess import call
from prettytable import PrettyTable
import platform
import cpuinfo

while True:

    call('clear')
	
    # Fetch the battery information
    battery = psutil.sensors_battery()
    
    print("----Battery: %d "%(battery.percent,) + "% "+ ("Changed" if battery.power_plugged else "No Changed" ))

	# We have used PrettyTable to print the data on console.
	# t = PrettyTable(<list of headings>)
	# t.add_row(<list of cells in row>)

	# Fetch the Network information
    print("----Networks----")
    table = PrettyTable(['Network', 'Status', 'Speed'])
    for key in psutil.net_if_stats().keys():
        name = key
        up = "Up" if psutil.net_if_stats()[key].isup else "Down"
        speed = psutil.net_if_stats()[key].speed
        table.add_row([name, up, speed])
    print(table)

	# Fetch the memory information
    print("----RAM (GB)----")
    memory_table = PrettyTable(["Total", "Used",
								"Available", "%"])
    vm = psutil.virtual_memory()
    memory_table.add_row([
        round(vm.total*10**-9,2),
        round(vm.used*10**-9,2),
        round(vm.available*10**-9,2),
        vm.percent
    ])
    print(memory_table)
	

	# Fetch the last 10 processes from available processes
    print("----Processes----")
    print("CPU: " + str(psutil.cpu_percent())+"%")
    process_table = PrettyTable(['PID', 'PNAME', 'STATUS',
                'CPU %', 'NUM THREADS'])
	
    for process in psutil.pids()[-10:]:

		# While fetching the processes, some of the subprocesses may exit
		# Hence we need to put this code in try-except block
        try:
            p = psutil.Process(process)
            process_table.add_row([
                str(process),
                p.name(),
                p.status(),
                p.cpu_percent(),
                p.num_threads()
                ])
			
        except Exception as e:
            pass
    print(process_table)

	# Create a 1 second delay
    time.sleep(2)
