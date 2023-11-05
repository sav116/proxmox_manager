from proxmoxer import ProxmoxAPI
from data.config import ProxmoxVMConfig
from paramiko import SSHClient, AutoAddPolicy
from utils.base import BaseMeta

class ProxmoxNode(metaclass=BaseMeta):
    
    def __init__(self, config: ProxmoxVMConfig):
        self.config = config

    def _get_proxmox(self):
        prox = ProxmoxAPI(
            self.config.hostname,
            user=self.config.username,
            password=self.config.password,
            verify_ssl=False,
        )
        return prox
        
    def get_vms(self) -> list:
        proxmox = self._get_proxmox()
        return proxmox.nodes(proxmox.nodes.get()[0]['node']).qemu.get()

    def get_vm(self) -> list:
        proxmox = self._get_proxmox()
        return proxmox.nodes(proxmox.nodes.get()[0]['node']).qemu.get()
    
    def get_vm_name(self, vmid: int) -> str:
        proxmox = self._get_proxmox()
        for vm in proxmox.nodes(proxmox.nodes.get()[0]['node']).qemu.get():
            if vm["vmid"] == vmid:
                return vm["name"]
    
    def start_vm(self, id) -> None:
        proxmox = self._get_proxmox()
        return proxmox.nodes(self.config.node_name).qemu(id).status.post("start")
        
    def shutdown_vm(self, id) -> None:
        proxmox = self._get_proxmox()
        return proxmox.nodes(self.config.node_name).qemu(id).status.post("shutdown")

    def reboot_vm(self, id) -> None:
        proxmox = self._get_proxmox()
        return proxmox.nodes(self.config.node_name).qemu(id).status.post("reboot")

    def status(self) -> str:
        proxmox = self._get_proxmox()
        return proxmox.nodes.get()[0]["status"]
    
    def _get_ssh_connect(self) -> SSHClient:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(self.config.hostname, username='root', password=self.config.password)
        return ssh
        
    def shutdown(self) -> None:
        self._get_ssh_connect().exec_command('shutdown')
    
    def reboot(self) -> None:
        self._get_ssh_connect().exec_command('reboot')