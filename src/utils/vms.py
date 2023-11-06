from data.loader import node
import math
import datetime

def get_vm_info(vmid: int) -> str:
    vm_info = node.get_vm(vmid)
    ram = int(vm_info['maxmem'] / math.pow(1024, 3))
    cpus = vm_info['cpus']
    uptime = str(datetime.timedelta(seconds=int(vm_info['uptime'])))
    status = vm_info['status']
    return f"{vm_info['name']}\nstatus: {status}\nram: {ram} Gb\ncpus: {cpus} cores\nuptime: {uptime} hours"