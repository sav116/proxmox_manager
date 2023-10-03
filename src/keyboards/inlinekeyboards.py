from aiogram.types import InlineKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from data.loader import node


status = {
    "running": "🟢",
    "stopped": "⚪️",
}

def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    for vm in sorted(node.get_vms(), key=lambda x: x['name']):
        vm_status = vm["status"]
        status_symbol = status[vm_status]
        text = f"{status_symbol} {vm['name']}"
        callback_data = f"ikb_vm_{vm['vmid']}"
        button = InlineKeyboardMarkup(text=text,
                                 callback_data=callback_data)
        ikb.add(button)
    return ikb

def get_ikb_vm(vmid: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    vm = [vm for vm in node.get_vms() if vm.get('vmid') == vmid][0]
        
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
        ikb.add(b1)
        ikb.add(b2)
        
    return ikb