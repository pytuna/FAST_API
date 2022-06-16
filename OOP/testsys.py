import psutil
import time
from prettytable import PrettyTable
from abc import ABC, abstractclassmethod
import datetime  
import pytz
from enum import Enum
from subprocess import call
from time import sleep
from ramMYSQL import connect_database, insert_info_ram

sleep(2)
tz_VN = pytz.timezone('Asia/Ho_Chi_Minh')

class System(ABC):
    @abstractclassmethod
    def update(self):
        pass
    @abstractclassmethod
    def show(self):
        pass

    def __str__(self) -> str:
        return type(self).__name__
    def __repr__(self) -> str:
        return super().__repr__()
class Condition():
    B = "Byte"
class Ram(System,object):
    
    def __init__(self, total=None, used=None, available=None, percent=None, *args, **kwargs) -> None:
        super().__init__()
        self.__total = total 
        self.__used = used
        self.__available = available
        self.__percent = percent
        self.__time = datetime.datetime.now(tz_VN).strftime("%Y-%m-%d/%H:%M:%S")
        self.__unit = Condition.B
    # Getter
    @property
    def total(self):
        return self.__total
    @property
    def used(self):
        return self.__used
    @property
    def available(self):
        return self.__available
    @property
    def percent(self):
        return self.__percent
    
    def show(self):
        print(self)

    def update(self,*,total, used, available, percent):
        self.__total = total 
        self.__used = used
        self.__available = available
        self.__percent = percent
        self.__time = datetime.datetime.now(tz_VN).strftime("%d-%m-%Y %H:%M:%S")
        self.__unit = Condition.B

    def insert_into_database(self):
        pass

    def unit_convert(self, unit:str):
        pass
    def __str__(self) -> str:
        temp = "Total: {0} {4}; Used: {1} {4}; Available: {2} {4}; Percent: {3}%".format(self.__total, self.__used, self.__available, self.__percent, self.__unit)
        return super().__str__()+" "+temp+" Time: "+self.__time

if __name__ == '__main__':
    while(1):   
        call('clear')
        print("----RAM (GB)----")
        memory_table = PrettyTable(["Total", "Used",
                                        "Available", "%"])
        vm = psutil.virtual_memory()
        ram = Ram()
        ram.update(total = vm.total,used = vm.used,available = vm.available,percent = vm.percent)

        memory_table.add_row([
                round(vm.total*10**-9,2),
                round(vm.used*10**-9,2),
                round(vm.available*10**-9,2),
                vm.percent
            ])
        print(memory_table)
        ram.show()
        
        sleep(1)
