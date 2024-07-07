from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.loader import dp, node, bot

class ChangeRAMStep(StatesGroup):
    waiting_for_new_ram = State()

@dp.callback_query_handler(lambda call: call.data.startswith("change_ram"))
async def change_ram(call: types.CallbackQuery, state: FSMContext):
    vmid = int(call.data.split("_")[-1])
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f"Введите новое значение памяти (GB) для VM {vmid}:")
    await state.update_data(vmid=vmid)
    await ChangeRAMStep.waiting_for_new_ram.set()

@dp.message_handler(state=ChangeRAMStep.waiting_for_new_ram, content_types=types.ContentTypes.TEXT)
async def process_new_ram_value(message: types.Message, state: FSMContext):
    new_ram_value = message.text
    if not new_ram_value.isdigit():
        await message.reply("Введите количество памяти (GB):")
        return
    new_ram_value_mb = int(new_ram_value) * 1024
    user_data = await state.get_data()
    vmid = user_data['vmid']
    node.update_vm_config(vmid, memory=new_ram_value_mb)
    await message.reply(f"Значение памяти для VM {vmid} обновлено до {new_ram_value}Gb.")
    await state.finish()
