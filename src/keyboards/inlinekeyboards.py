from aiogram.types import InlineKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from data.loader import node


status = {
    "running": "🟢",
    "stopped": "⚪️",
}

def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    
    for vm in sorted(node.get_vms(), key=lambda x: x['name']):
        if "template" not in vm['name']:
            vm_status = vm["status"]
            status_symbol = status[vm_status]
            text = f"{status_symbol}{vm['vmid']} {vm['name']}"
            callback_data = f"ikb_vm_{vm['vmid']}"
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            buttons.append(button)
        
    ikb.add(*buttons)
    update_vm_button = InlineKeyboardButton(text="🔄", callback_data="update_vm_buttons")
    
    ikb.add(update_vm_button)
    
    return ikb

def get_ikb_vm(vmid: int) -> InlineKeyboardMarkup:

    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    vm = [vm for vm in node.get_vms() if vm.get('vmid') == vmid][0]
    main_action = "configure"
    b_config = InlineKeyboardMarkup(text=main_action + " ⚙️",
                            callback_data=f"{main_action}_{vm['vmid']}")
    # ikb.add(b_config)

    main_action = "delete"
    d_config = InlineKeyboardMarkup(text=main_action + " 🗑️",
                            callback_data=f"{main_action}_{vm['vmid']}")
    
    ikb.add(b_config, d_config)

    if vm["status"] == "stopped":
        main_action = "start"
        b = InlineKeyboardMarkup(text=main_action + " ▶️",
                                 callback_data=f"{main_action}_{vm['vmid']}")
        ikb.add(b)
    else:
        main_action = "reboot"
        b1 = InlineKeyboardMarkup(text=main_action + " 🔄",
                                  callback_data=f"{main_action}_{vm['vmid']}")
        main_action = "shutdown" + " ⏹️"
        b2 = InlineKeyboardMarkup(text=main_action,
                                  callback_data=f"{main_action}_{vm['vmid']}")
        ikb.add(b1, b2)
        
    return ikb

def get_config_ikb_vm(vmid: int) -> InlineKeyboardMarkup:
    
    ikb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    main_action  = "change_cpu"
    b_cpu = InlineKeyboardMarkup(text="cpu",
                                callback_data=f"{main_action}_{vmid}")
    main_action  = "change_ram"
    b_ram = InlineKeyboardMarkup(text="ram",
                                callback_data=f"{main_action}_{vmid}")
    main_action  = "resize_disk"
    b_resize_disk = InlineKeyboardMarkup(text="resize disk",
                                callback_data=f"{main_action}_{vmid}")
    main_action  = "add_new_disk"
    b_add_new_disk = InlineKeyboardMarkup(text="add new disk",
                                callback_data=f"{main_action}_{vmid}")
    
    ikb.add(b_cpu, b_ram, b_resize_disk, b_add_new_disk)
    return ikb
