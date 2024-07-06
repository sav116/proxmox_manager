from data.config import config
from utils.proxmox import ProxmoxNode
import time

node = ProxmoxNode(config)
proxmox = node._get_proxmox()

vmid = 161

# Остановка виртуальной машины
print(f"Остановка виртуальной машины с ID {vmid}...")
proxmox.nodes(config.node_name).qemu(vmid).status.stop.post()

# Ожидание, пока виртуальная машина не остановится
vm_stopped = False
while not vm_stopped:
    status = proxmox.nodes(config.node_name).qemu(vmid).status.current.get()
    if status['status'] == 'stopped':
        vm_stopped = True
    else:
        time.sleep(3)

# Удаление виртуальной машины
print(f"Удаление виртуальной машины с ID {vmid}...")
proxmox.nodes(config.node_name).qemu(vmid).delete()

print(f"Виртуальная машина с ID {vmid} удалена.")
