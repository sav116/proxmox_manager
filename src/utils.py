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
        import requests
        reboot_url = f'https://{self.config.hostname}:8006/api2/extjs/nodes/proxmox/status/reboot'
        session = requests.Session()
        session.verify = False
        # Вход в систему Proxmox
        login_url = f'https://{self.config.hostname}:8006/api2/json/access/ticket'
        data = {'username': self.config.username, 'password': self.config.password}
        response = session.post(login_url, data=data)
        response.raise_for_status()
        ticket_data = response.json()
        ticket = ticket_data['data']['ticket']
        csrf_token = ticket_data['data']['CSRFPreventionToken']
        headers = {'CSRFPreventionToken': csrf_token, 'Cookie': f'PVEAuthCookie={ticket}'}

        response = session.post(reboot_url, headers=headers)
        response.raise_for_status()

        # Проверка успешности перезагрузки
        if response.status_code == 200:
            print("Нода успешно перезагружается.")
        else:
            print("Не удалось перезагрузить ноду. Код ошибки:", response.status_code)

        #self.proxmox.nodes(self.config.node_name).status.reboot()
        #print(s)

