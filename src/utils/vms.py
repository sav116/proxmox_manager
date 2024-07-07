from data.loader import node
import math
import datetime

def get_vm_info(vmid: int) -> str:
    vm_info = node.get_vm(vmid)
    vm_conf = node.get_vm_config(vmid)
    ram = int(vm_info['maxmem'] / math.pow(1024, 3))
    cpus = vm_info['cpus']
    uptime = str(datetime.timedelta(seconds=int(vm_info['uptime'])))
    status = vm_info['status']
    vm_id = vm_info['vmid']
    reult = f"""id: {vm_id}
name: {vm_info['name']}
status: {status}
ram: {ram} GB
cpus: {cpus} cores
uptime: {uptime}"""
    disks = []
    for i in vm_conf:
        if 'scsi' in i and i[-1].isdigit():
            disks.append(vm_conf[i])
            reult += f"\n{vm_conf[i]}"

    return reult


