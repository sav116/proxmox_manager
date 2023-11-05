from utils.logger_base import logger_decorator
from data.loader import node

@logger_decorator
def start_k8s() -> None:
    for vm in node.get_vms():
        if vm['name'].startswith('k8s'):
            node.start_vm(vm['vmid'])
            