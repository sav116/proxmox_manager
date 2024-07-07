from data.config import config
from utils.proxmox import ProxmoxNode

# Инициализация ProxmoxNode
node = ProxmoxNode(config)
proxmox = node._get_proxmox()

# # Идентификатор виртуальной машины и размер инкремента
vmid = 180
storage="ssd1"
input_value=10

node.create_new_disk(vmid, storage, size=f"{input_value}G")

# increase_size_gb = 10  # Размер увеличения в ГБ

# # Имя диска
# disk_name = "scsi0"

# # Получение текущей конфигурации диска
# vm_config = proxmox.nodes(node.name).qemu(vm_id).config.get()

# Получаем информацию о текущем размере диска
# current_size = None
# for key, value in vm_config.items():
#     if key == disk_name:
#         current_size_str = value.split(",")[1].split("=")[1]
#         current_size = int(current_size_str[:-1])  # удаляем 'G' и преобразуем в int
#         break

# if current_size is None:
#     print(f"No disk found with name {disk_name} for VM {vm_id}")
# else:
#     new_size_gb = current_size + increase_size_gb

#     # Изменяем размер диска
#     try:
#         proxmox.nodes(node.name).qemu(vm_id).resize.put(
#             disk=disk_name,
#             size=f'+{increase_size_gb}G'
#         )
#         print(f"Successfully increased disk {disk_name} by {increase_size_gb} GB for VM {vm_id}")
#     except Exception as e:
#         print(f"Failed to resize disk: {e}")


# Получаем информацию о хранилище
# storage_info = proxmox.nodes(node.name).storage(storage_name).status.get()
# available_space_gb = int(storage_info['avail']) / (1024 ** 3)

# if available_space_gb < new_disk_size_gb:
#     print(f"Not enough space in storage {storage_name} for a new {new_disk_size_gb} GB disk.")
# else:
#     # Ищем свободный слот для нового диска
#     vm_config = proxmox.nodes(node.name).qemu(vm_id).config.get()
#     disk_id = None
#     for i in range(16):
#         scsi_key = f"scsi{i}"
#         if scsi_key not in vm_config:
#             disk_id = scsi_key
#             break

#     if disk_id is None:
#         print(f"No free disk slot available for VM {vm_id}")
#     else:
#         # Создаем новый диск на хранилище
#         disk_name = f"vm-{vm_id}-disk-{disk_id}"
#         proxmox.nodes(node.name).storage(storage_name).content.post(
#             vmid=vm_id,
#             filename=disk_name,
#             size=f"{new_disk_size_gb}G"  # размер в ГБ
#         )

#         # Привязываем созданный диск к виртуальной машине
#         proxmox.nodes(node.name).qemu(vm_id).config.post(
#             **{disk_id: f"{storage_name}:{disk_name},size={new_disk_size_gb}G"}
#         )

#         print(f"Successfully added {new_disk_size_gb} GB disk {disk_id} on storage {storage_name} to VM {vm_id}")
