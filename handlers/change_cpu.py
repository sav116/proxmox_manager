from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.loader import dp, node, bot

class ChangeCPUStep(StatesGroup):
    waiting_for_new_cpu = State()

@dp.callback_query_handler(lambda call: call.data.startswith("change_cpu"))
async def change_cpu(call: types.CallbackQuery, state: FSMContext):
    vmid = int(call.data.split("_")[-1])
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f"Введите новое значение CPU для VM {vmid}:")
    await state.update_data(vmid=vmid)
    await ChangeCPUStep.waiting_for_new_cpu.set()

@dp.message_handler(state=ChangeCPUStep.waiting_for_new_cpu, content_types=types.ContentTypes.TEXT)
async def process_new_cpu_value(message: types.Message, state: FSMContext):
    new_cpu_value = message.text
    if not new_cpu_value.isdigit():
        await message.reply("Введите количество ядер CPU:")
        return
    new_cpu_value = int(new_cpu_value)
    user_data = await state.get_data()
    vmid = user_data['vmid']
    node.update_vm_config(vmid, cores=new_cpu_value)
    await message.reply(f"Количество ядер CPU для VM {vmid} обновлено до {new_cpu_value}.")
    await state.finish()
