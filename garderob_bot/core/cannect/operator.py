from aiogram import Bot
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext

from core.data_base.db import cur,conn
from core.config.data import operator,operators
from core.keyboards.inline import ask_one_question_kb
from core.utils.statesform import StepsMailing,StatesCustomer,StatesOperator,StatesOpDB
from core.data_base.orders import db_shut_protect,db_protect
is_operator_online = False
waiting = []
chatting = []
operators_online = []
waiting_for_reply = []

connections = [[],[]]
pre_offers = [[],[]]


mailtxt:str
mail_photo_url:str


async def answer_toa_question(message:Message,bot:Bot):
    # if str(message.from_user.id) == operator:
    if message.from_user.id in operators:
        id = message.text.split()[1]
        msg = 'Ответ оператора:\n'+message.text.split(id)[1]
        id = int(id)
        if id in waiting_for_reply:
        # print(msg)
            waiting_for_reply.remove(id)
            for i in range(len(operators_online)):
                if operators_online[i] != message.from_user.id:
                    await bot.send_message(chat_id = operators[i],text=f'{message.from_user.first_name} ответил на сообщение пользователя {id}. Вопрос больше <b>не активен</b>')
            await bot.send_message(chat_id=id,text = msg)
            await message.answer('Ответ отправлен')
        else:
            await message.answer('На сообщения этого пользователя <b>уже ответили</b>')

async def anspic(message:Message,bot:Bot):
    if message.from_user.id in operators:
        id = message.caption.split()[1]
        msg = 'Ответ оператора:\n'+message.caption.split(id)[1]
        phid = message.photo[-1].file_id
        id = int(id)
        if id in waiting_for_reply:
        # print(msg)
            waiting_for_reply.remove(id)
            for i in range(len(operators_online)):
                if operators_online[i] != message.from_user.id:
                    await bot.send_message(chat_id = operators[i],text=f'{message.from_user.first_name} ответил на сообщение пользователя {id}. Вопрос больше <b>не активен</b>')
            await bot.send_photo(chat_id=id,photo = phid,caption = msg)
            await message.answer('Ответ отправлен')
        else:
            await message.answer('На сообщения этого пользователя <b>уже ответили</b>')
async def op_online(message: Message, state:FSMContext):
    global operators_online
    # if str(message.from_user.id) == operator
    if message.from_user.id in operators:
        if not message.from_user.id in operators_online:
            global is_operator_online
            operators_online.append(message.from_user.id)
            is_operator_online = True
            # await state.set_state(StatesOperator.ONLINE)
            # print(await state.get_state())
            await message.answer('Теперь Вы <b>онлайн</b> и клиенты <b>могут</b> Вам написать')
        else:
            await message.answer('Вы уже включили режим онлайн')

async def op_offline(message:Message,state:FSMContext):
    global operators_online
    # if str(message.from_user.id) == operator:
    if message.from_user.id in operators:
        if message.from_user.id in operators_online:
            global is_operator_online
            operators_online.remove(message.from_user.id)
            is_operator_online = False
            # await state.set_state(StatesOperator.OFFLINE)
            # print(await state.get_state() == StatesOperator.OFFLINE)
            await message.answer('Теперь Вы <b>оффлайн</b> и клиенты <b>не</b> могут Вам написать')
        else: await message.answer('Ваш режим - <b>оффлайн</b>')

async def dyalog_start_or_drop(call:CallbackQuery,bot:Bot,state:FSMContext):
    global is_operator_online
    global operators_online
    global waiting
    # if is_operator_online == True:
    if call.from_user.id not in waiting:
        if call.from_user.id not in connections[1]:
            if len(operators_online)>0:
                name:str
                add:str
                add = 'Пользователь без заказов'
                if call.from_user.id in pre_offers[0]:
                    ind = pre_offers[0].index(call.from_user.id)
                    name = pre_offers[1][ind]
                    add = f'Заказ клиента: {name}'
                    pre_offers[0].remove(call.from_user.id)
                    pre_offers[1].remove(name)

                for i in range(len(operators_online)):
                    await bot.send_message(chat_id=operators_online[i],
                                           text = f'{add}\nПользователь {call.from_user.first_name}, ID: {call.from_user.id} ожидает подключения к диалогу.\n/accept для старта диалога')
                # await bot.send_message(chat_id=operator,
                #                        text=f'пользователь {call  .from_user.id} ожидает подключения. /accept_{call.from_user.id} чтобы начать')
                waiting.append(call.from_user.id)

                await call.message.answer('Заявка сформирована. Ожидайте подключения оператора...')
                await call.answer()

            # elif is_operator_online != True:
            elif len(operators_online) == 0:
                await call.message.edit_text('К сожалению, на данный момент все операторы находятся не в сети и не могут ответить. Но Вы можете задать вопрос на который ответит первый появившейся в сети оператор.\n\n'
                                          'Напишите свой вопрос одним следующим сообщением или дождитесь времени работы операторов и попробуйте нажать кнопку <b>"Оставить сообщение"</b> снова.'
                                            , reply_markup=ask_one_question_kb)
                await call.answer()
        else:
            name: str
            if call.from_user.id in pre_offers[0]:
                ind = pre_offers[0].index(call.from_user.id)
                name = pre_offers[1][ind]
                pre_offers[0].remove(call.from_user.id)
                pre_offers[1].remove(name)
                ind = connections[1].index(call.from_user.id)

                await call.message.edit_text('Товар передан оператору')
                await bot.send_message(chat_id=connections[0][ind],text ='Товар от пользователя'+' '+str(call.from_user.id)+' '+name[1:])
                pre_offers[0].remove(call.from_user.id)
                pre_offers[1].remove(name)
                await call.answer()
            else:
                await call.message.answer('Вы уже ведёте диалог с оператором')
                await call.answer()
    else:
        await call.message.answer('Извините, но Вы уже отправили заявку на диалог с оператором.')
        await call.answer()


async def accept_conv(message:Message,bot:Bot):
    global waiting
    if message.from_user.id in operators_online and len(waiting)!=0:
    # if str(message.from_user.id) == operator:

        global chatting
        await bot.send_message(chat_id=str(waiting[0]),text = 'Оператор принял Ваш запрос! Сессия диалога установлена. Помните, оператор не получает стикеры и голосовые сообщения от Вас.')
        await message.answer(f'Диалог c {str(waiting[0])} установлен.<b>Напишите приветствие клиенту</b>. Для удобства копируйте команды ниже и допишите после них необходимый текст или прикрепите фотографию')
        await message.answer(f'<code>/reply {str(waiting[0])}</code>')
        await message.answer(f'<code>/replypic {str(waiting[0])}</code>')
        chatting.append(waiting[0])

        connections[0].append(message.from_user.id)
        connections[1].append(waiting[0])

        waiting.pop(0)
        for i in range(len(operators_online)):
            if operators_online[i] != message.from_user.id:
              await bot.send_message(chat_id=operators_online[i],text=f'{message.from_user.first_name} начал диалог c {waiting[0]}. Запрос больше не активен.')
    elif message.from_user.id in operators:
        await message.answer('Вы не включили онлайн режим, либо все заявки уже приняты')


async def op_pic_reply(message:Message,bot:Bot):
    if message.from_user.id in connections[0]:
        cust_id = int(message.caption.split()[1])
        if connections[0].count(message.from_user.id) == 1:
            ind = connections[0].index(message.from_user.id)
            if ind == int(connections[1].index(int(message.caption.split()[1]))):
                fid = message.photo[-1].file_id
                msg = f'Сообщение от оператора:\n{message.caption.split(message.caption.split()[1])[1]}'
                await bot.send_photo(chat_id=message.caption.split()[1],photo=fid  , caption = msg)
        else:
            ind = []
            for i in range(len(connections[0])):
                if connections[0][i]==message.from_user.id:
                    ind.append(i)
            cust_ind = connections[1].index(cust_id)
            if cust_ind in ind:
                fid = message.photo[-1].file_id
                msg = f'Сообщение от оператора:\n{message.caption.split(message.caption.split()[1])[1]}'
                await bot.send_photo(chat_id=message.caption.split()[1],photo=fid, caption=msg)


async def op_msg_reply(message:Message,bot:Bot):
    if message.from_user.id in connections[0]:
        cust_id = int(message.text.split()[1])
    # if str(message.from_user.id) == operator:
        if connections[0].count(message.from_user.id) == 1:
            ind = connections[0].index(message.from_user.id)
            if ind == int(connections[1].index(int(message.text.split()[1]))):
                msg = f'Сообщение от оператора:\n{message.text.split(message.text.split()[1])[1]}'
                await bot.send_message(chat_id=message.text.split()[1], text=msg)
        else:
            ind = []
            for i in range(len(connections[0])):
                if connections[0][i]==message.from_user.id:
                    ind.append(i)
            cust_ind = connections[1].index(cust_id)
            if cust_ind in ind:
                msg = f'Сообщение от оператора:\n{message.text.split(message.text.split()[1])[1]}'
                await bot.send_message(chat_id=message.text.split()[1], text=msg)





async def close_conv(message:Message,bot:Bot):
    # if str(message.from_user.id) == operator:
    if message.from_user.id in connections[0]:
        cust_id = int(message.text.split()[1])
        global chatting
        if cust_id in chatting:
            chatting.remove(cust_id)
            connections[0].remove(message.from_user.id)
            connections[1].remove(cust_id)
            await bot.send_message(chat_id=message.text.split()[1], text='Диалог завершен. Спасибо за обращение, мы всегда Вам рады!')
            await bot.send_message(chat_id=message.from_user.id, text='Диалог завершен. Сессия разорвана. Спасибо за работу!')

async def begin_mailing(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await message.answer("Введите текст для рассылки")
        await state.set_state(StepsMailing.INSERT_TEXT)

async def get_mailing_text(message:Message,state:FSMContext,bot:Bot):
    await message.answer('Прикрепите медиа-файл, затем /send)')
    global mailtxt
    mailtxt = str(message.text)
    await state.set_state(StepsMailing.INSERT_MEDIA)


async def send_mailing(message:Message,bot:Bot):
    db_protect("SELECT COUNT(*) FROM mailing")
    cur.execute("SELECT COUNT(*) FROM mailing")
    num = int(cur.fetchone()[0])
    db_protect("SELECT user_id FROM mailing")
    cur.execute("SELECT user_id FROM mailing")
    cust = [int(x[0]) for x in cur.fetchall()]
    for i in range(num):
        db_protect(f"SELECT COUNT(user_id) FROM mailing_check WHERE user_id = '{cust[i]}'")
        cur.execute(f"SELECT COUNT(user_id) FROM mailing_check WHERE user_id = '{cust[i]}'")
        if int(cur.fetchone()[0]) == 0:
            db_protect(f"SELECT mailing_state FROM mailing WHERE user_id = '{cust[i]}' ORDER BY ser_num DESC LIMIT 1")
            cur.execute(f"SELECT mailing_state FROM mailing WHERE user_id = '{cust[i]}' ORDER BY ser_num DESC LIMIT 1")
            if cur.fetchone()[0]:
                await bot.send_photo(chat_id=str(cust[i]), photo=mail_photo_url, caption=mailtxt)
                cur.execute(f"INSERT INTO mailing_check VALUES ({cust[i]})")
                conn.commit()
    await message.answer('Рассылка успешно создана!')
    cur.execute("TRUNCATE TABLE mailing_check")
async def get_mailing_pic(message:Message,bot:Bot):
    global mail_photo_url
    mail_photo_url = str(message.photo[-1].file_id)


async def insert_cust_info(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await message.answer('Введите информацию о пользователе построчно:\n1)ID пользователя.\n2)ФИО\n3)Мобильный номер телефона\n4)Адрес электронной почты')
        await state.set_state(StatesOpDB.INSERT_INFO)

async def get_cust_info(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await message.answer('Введите ID <b>пользователя</b> для получиения информации о нем')
        await state.set_state(StatesOpDB.GET_INFO)

async def add_order(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await state.set_state(StatesOpDB.ADD_ORDER)
        await message.answer('Введите информацию о заказе построчно:\n1)ID клиента\n2)ID заказа \n3)Название товара\n4)Размер\n5)Стоимсть\n6)Скидка\n7)Дата\n8)Адрес')

async def get_order(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await state.set_state(StatesOpDB.GET_ORDER)
        await message.answer('Введите ID <b>заказа</b> для получения информации о нем')

async  def get_orders(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await state.set_state(StatesOpDB.GET_ORDERS)
        await message.answer('Введите ID <b>пользователя</b>, чтобы увидеть <b>все</b> его заказы')

async def set_status(message:Message,state:FSMContext):
    if message.from_user.id in operators:
        await state.set_state(StatesOpDB.SET_ORDER_STATE)
        await message.answer('Введите ID <b>заказа</b> для которого хотите установить или изменить статус. Если есть трек-код, пропишите его в конце. <b>Статус через ТИРЕ</b>\nПример:[ID]-[текст] [трек-код] (в квадратные скобки вставить нужное)')


# async def check(message:Message):
#     await message.answer(message.photo[-1].file_id)


async def send_msg(message:Message,bot:Bot):
    if message.from_user.id in operators:
        txt = message.text
        uid = txt.split()[1]
        msg = 'Сообщение от оператора:\n'+txt.split(uid)[1]
        try:
            await bot.send_message(chat_id=uid,text=msg)
            await message.answer('Сообщение отправлено')
        except:
            await message.answer('Ошибка, проверьте введенные данные')
