from utils import ProxmoxNode
from config import config

def main():
    node = ProxmoxNode(config)
    node.status()
    node.get_vms()
    node.start_vm(130)
    node.shutdown_vm(130)
    
if __name__ == "__main__":
    main()