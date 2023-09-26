from proxmoxer import ProxmoxAPI
from config import ProxmoxVMConfig, logger_decorator

class ProxmoxNode:
    def __init__(self, config: ProxmoxVMConfig):
        self.config = config
        self.proxmox = ProxmoxAPI(
            self.config.hostname,
            user=config.username,
            password=config.password,
            verify_ssl=False,
        )
        
    @logger_decorator
    def get_vms(self) -> list:
        return self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get()

    @logger_decorator
    def start_vm(self, id) -> None:
        self.proxmox.nodes(self.config.node_name).qemu(id).status.post("start")
        
    @logger_decorator
    def shutdown_vm(self, id) -> None:
        self.proxmox.nodes(self.config.node_name).qemu(id).status.post("shutdown")

    @logger_decorator
    def reboot_vm(self, id) -> None:
        self.proxmox.nodes(self.config.node_name).qemu(id).status.post("reboot")

    @logger_decorator
    def status(self) -> str:
        return self.proxmox.nodes.get()[0]["status"]
    
    @logger_decorator
    def reboot(self) -> None:
        pass
