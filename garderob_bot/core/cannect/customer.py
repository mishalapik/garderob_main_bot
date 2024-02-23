from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StatesCustomer
from core.config.data import operator,operators
from core.cannect.operator import connections,chatting,pre_offers
from core.keyboards.inline import pre_offer_kb,backto_help_kb


from core.config.data import admin_id
from core.data_base.db import cur,conn





askers = []





async def cust_chat(message:Message,bot:Bot):
    if message.from_user.id in chatting:
        if message.from_user.id in connections[1]:
            ind = connections[1].index(message.from_user.id)
            op_id = connections[0][ind]
            msg = f'Сообщение пользователя <code>{message.from_user.id}</code>:\n{message.text}'
            # msg = f'сообщение от {message.from_user.id}:\n{message.text}'
            await bot.send_message(chat_id=op_id,text=msg)
    else:await message.answer('Я вас не понимаю(')



async def send_question(message:Message,bot:Bot,state:FSMContext):
    # msg_for_op = 'вопрос от '+str(message.from_user.id)+':\n'+message.text
    # await bot.send_message(chat_id = operator,text = msg_for_op)
    
    if str(message.photo) == 'None':
        msg_for_op = f'Пользователь { str(message.from_user.id)} оставил сообщение, когда все операторы были оффлайн:\n{message.text}\nДля удобства копируйте команды ниже и допишите после них необходимый текст или прикрепите фотографию'
        for i in range(len(operators)):
            await bot.send_message(chat_id=operators[i], text=msg_for_op)
            await bot.send_message(chat_id=operators[i], text=f'<code>/answer {str(message.from_user.id)}</code>')
            await bot.send_message(chat_id=operators[i], text=f'<code>/answerpic {str(message.from_user.id)}</code>')
    else:
        msg_for_op = f'Пользователь { str(message.from_user.id)} оставил сообщение, когда все операторы были оффлайн:\n{message.caption}\nДля удобства копируйте команды ниже и допишите после них необходимый текст или прикрепите фотографию'
        for i in range(len(operators)):
            await bot.send_photo(chat_id=operators[i],photo=message.photo[-1].file_id, caption=msg_for_op)
            await bot.send_message(chat_id=operators[i], text=f'<code>/answer {str(message.from_user.id)}</code>')
            await bot.send_message(chat_id=operators[i], text=f'<code>/answerpic {str(message.from_user.id)}</code>')

    await message.answer('Ваше сообщение отправлено. Первый появившийся в сети оператор ответит на него.\nОператоры работают с 8:00 до 21:00 по МСК в будние дни и в выходные с 9:00 до 20:00 по МСК.',reply_markup=backto_help_kb)
    await state.set_state(StatesCustomer.NONE)
async def confirm_offer(message:Message,bot:Bot):
    name = str(message.caption).split('\n')[0]
    if name != 'None':
        if 'ЗАКАЗАТЬ' in message.caption:
            await message.answer(f'Вы переслали сообщение из Гардероб.shop. Желаете заказать {name[1:]}?',reply_markup=pre_offer_kb)
            pre_offers[0].append(message.from_user.id)
            pre_offers[1].append(name)
        elif message.from_user.id in connections[0] and message.caption.split()[0] == '/replypic':
            cust_id = int(message.caption.split()[1])
            if connections[0].count(message.from_user.id) == 1:
                ind = connections[0].index(message.from_user.id)
                if ind == int(connections[1].index(int(message.caption.split()[1]))):

                    fid = message.photo[-1].file_id
                    msg = f'Сообщение от оператора:\n{message.caption.split(message.caption.split()[1])[1]}'
                    await bot.send_photo(chat_id=message.caption.split()[1], photo=fid, caption=msg)
            elif message.caption.split()[0] == '/replypic':
                ind = []
                for i in range(len(connections[0])):
                    if connections[0][i] == message.from_user.id:
                        ind.append(i)
                cust_ind = connections[1].index(cust_id)
                if cust_ind in ind:
                    # print(1)
                    fid = message.photo[-1].file_id
                    msg = f'Сообщение от оператора:\n{message.caption.split(message.caption.split()[1])[1]}'
                    await bot.send_photo(chat_id=message.caption.split()[1], photo=fid, caption=msg)

        elif message.from_user.id in connections[1] and message.from_user.id in chatting:
            ind = connections[1].index(message.from_user.id)
            op_id = connections[0][ind]
            msg = f'Сообщение пользователя <code>{message.from_user.id}</code>:\n{message.caption}'
            # msg = f'сообщение от {message.from_user.id}:\n{message.text}'
            await bot.send_photo(chat_id=op_id,photo = message.photo[-1].file_id ,caption=msg)


    # askers.remove(message.from_user.id)
    # elif message.from_user.id in chatting:
    #     msg = f'сообщение от {message.from_user.id}:\n{message.text}'
    #     await bot.send_message(chat_id=operator,text = msg)
# print(type(askers[0]),askers[0],type(message.from_user.id),message.from_user.id)




