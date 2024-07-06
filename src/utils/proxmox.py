from proxmoxer import ProxmoxAPI
from paramiko import SSHClient, AutoAddPolicy

import time

from data.config import ProxmoxVMConfig
from utils.logger_base import logger
from utils.base import BaseMeta

class ProxmoxNode(metaclass=BaseMeta):
    
    def __init__(self, config: ProxmoxVMConfig):
        self.config = config
        self.proxmox = self._get_proxmox()

    def _get_proxmox(self):
        return ProxmoxAPI(
            self.config.hostname,
            user=self.config.username,
            password=self.config.password,
            verify_ssl=False,
        )

    def _execute_ssh_command(self, ip: str, username: str, password: str, command: str):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            logger.info(f"Connecting to {ip}...")
            ssh.connect(ip, username=username, password=password)
            logger.info("Connected successfully.")
            logger.info(f"Executing command: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            stdout_data = stdout.read().decode()
            stderr_data = stderr.read().decode()
            logger.info(stdout_data)
            logger.info(stderr_data)
            return stdout_data, stderr_data
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            ssh.close()

    def get_templates(self) -> list:
        return [vm for vm in self.get_vms() if 'template' in vm]
        
    def get_vms(self) -> list:
        return self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get()

    def get_vm(self, vmid: int) -> dict:
        for vm in self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get():
            if vm["vmid"] == vmid:
                return vm

    def update_vm_config(self, vmid, cores, memory):
        self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu(vmid).config.put(
            cores=cores,
            memory=memory
        )
    
    def create_vm_from_template(self, vmname: str, template_name: str, cores: int = 0, memory: int = 0, vmid: int = 0) -> None:
        newid = str(int(self.proxmox.cluster.nextid.get()) + 1)
        if vmid:
            newid = str(vmid)

        logger.info(f"Creating VM {vmname} with vmid {newid}")
        
        template_vmid = self.get_vmid_by_name(vmname=template_name)
        self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu(template_vmid).clone.post(
            newid=newid,
            name=vmname,
            full=1,
        )

        lock = True
        while lock:
            vm_info = self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu(newid).status.current.get()
            if "lock" in vm_info:
                time.sleep(3)
            else:
                lock = False

        logger.info(f"VM {vmname} with vmid {newid} created")

        if cores or memory:
            self.update_vm_config(newid, cores=cores, memory=memory)
        
        self.start_vm(newid)
        logger.info(f"Sleeping 10 seconds ...")
        time.sleep(10)
        self.change_hostname_and_ip(newid, vmname)
        self.reboot_vm(newid)

    def change_hostname_and_ip(self, vmid: int, vmname: str) -> None:
        self._execute_ssh_command(self.config.template_ip, 
                                  self.config.template_user,
                                  self.config.template_password,
                                  f"echo {vmname} > /etc/hostname")
        self._execute_ssh_command(self.config.template_ip, 
                                  self.config.template_user, 
                                  self.config.template_password,
                                  f"sed -i 's/\\.201$/\\.{vmid}/' /etc/sysconfig/network-scripts/ifcfg-ens18")

    def get_vmid_by_name(self, vmname: str) -> int:
        for vm in self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get():
            if vm["name"] == vmname:
                return vm["vmid"]
    
    def get_vm_name(self, vmid: int) -> str:
        for vm in self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get():
            if vm["vmid"] == vmid:
                return vm["name"]
    
    def start_vm(self, vmid) -> None:
        self.proxmox.nodes(self.config.node_name).qemu(vmid).status.post("start")
        for vm in self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get():
            if vm["vmid"] == vmid and vm["status"] == "running":
                logger.info(f"VM {vmid} is running")
                return
        
    def shutdown_vm(self, vmid) -> None:
        self.proxmox.nodes(self.config.node_name).qemu(vmid).status.post("shutdown")

    def reboot_vm(self, vmid) -> None:
        self.proxmox.nodes(self.config.node_name).qemu(vmid).status.post("reboot")
        for vm in self.proxmox.nodes(self.proxmox.nodes.get()[0]['node']).qemu.get():
            if vm["vmid"] == vmid and vm["status"] == "running":
                logger.info(f"VM {vmid} is running")
                return

    def status(self) -> str:
        return self.proxmox.nodes.get()[0]["status"]

    def start_k8s(self) -> None:
        for vm in self.get_vms():
            if vm['name'].startswith('k8s'):
                self.start_vm(vm['vmid'])

    def _get_ssh_connect(self, ip: str) -> SSHClient:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ip, username='root', password=self.config.password)
        return ssh
        
    def shutdown(self) -> None:
        self._get_ssh_connect(self.config.hostname).exec_command('shutdown')
    
    def reboot(self) -> None:
        self._get_ssh_connect(self.config.hostname).exec_command('reboot')
