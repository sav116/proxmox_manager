from utils.proxmox import ProxmoxNode
from data.config import config

def main():
    
    node = ProxmoxNode(config)
    node.status()
    node.get_vms()
    node.start_vm(130)
    node.shutdown_vm(130)
    #node.reboot()
    # node.shutdown()
    
if __name__ == "__main__":
    main()