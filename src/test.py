from data.config import config
from utils.proxmox import ProxmoxNode
import time


node = ProxmoxNode(config)
proxmox = node._get_proxmox()

vmid = 104
vmname='new-test-vm'
node.create_vm_from_template(
    vmname='bla-bla',
    template_name='alma-template-32g',
    vmid=vmid,)


node.change_hostname_and_ip(vmid, vmname)
#node.reboot_vm(vmid)