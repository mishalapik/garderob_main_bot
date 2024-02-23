from aiogram import Bot
import psycopg2
from aiogram.types import Message
from core.data_base.db import cur,conn
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StatesOpDB

def num_check(a:str):
    num = '0123456789'
    for i in a:
        if i not in num:
            return False
    return True

def db_shut_protect():
    global conn
    global cur
    queries = ['select count(*) from customer_info', 'select count(*) from orders']
    for query in queries:
        try:
            cur.execute(query)
        except psycopg2.ProgrammingError as exc:
            conn.rollback()
        except psycopg2.InterfaceError as exc:
            conn = psycopg2.connect(database='garderob_main_db',user='postgres',host='localhost',port='5432',password='yesterday')
            cur = conn.cursor()
        except psycopg2.OperationalError:
            conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                    password='yesterday')
            cur = conn.cursor()
        except psycopg2.errors.InFailedSqlTransaction:
            conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                    password='yesterday')
            cur = conn.cursor()

def db_protect(query:str):
    global conn
    global cur
    try:
        cur.execute(query)
    except psycopg2.ProgrammingError as exc:
        conn.rollback()
    except psycopg2.InterfaceError as exc:
        conn = psycopg2.connect(database='garderob_main_db',user='postgres',host='localhost',port='5432',password='yesterday')
        cur = conn.cursor()
    except psycopg2.OperationalError:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
    except psycopg2.errors.InFailedSqlTransaction:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()

async def set_cust_info(message:Message,state:FSMContext):
    await state.set_state(StatesOpDB.NONE)
    if len(message.text.split('\n')) == 4:
        cid,cfio,phone,mail = message.text.split('\n')
        if ' ' in cid:
            cid = cid.split()[0]
        # if num_check(cid) and len(mail)<64 and not ',' in phone and not ',' in mail:
        if num_check(cid) and len(mail) < 64 and not ',' in phone and not ',' in mail and not '\'' in cfio and not '\'' in phone and not '\'' in mail:
            if num_check(cid):
                db_protect(f"SELECT(customer_id) FROM customer_info")
                cur.execute(f"INSERT INTO customer_info (customer_id,customer_fio,phone_number,mail) VALUES ({cid},'{cfio}','{phone}','{mail}')")
                conn.commit()
                await message.answer('Данные о пользователе сохранены')
            else:await message.answer('Вводимый ID пользователя должен состоять <b>только</b> из цифр!')
        else:await message.answer('Неверный формат данных! Ограничения:\nID состоит <b>только</b> из цифр!\nВ полях ФИО, Телефона и Почты <b>не должно</b> быть запятых, апострофов или слешей (,/)')
    else: await message.answer('Введено неверное количество аргументов! Должно быть 4 строки:\nID пользователя\nФИО\nНомер телефона\nАдрес электронной почты')

async def show_cust_info(message:Message,state:FSMContext):
    if len(message.text.split()) == 1:
        if num_check(message.text):
            db_protect(f"SELECT COUNT(*) FROM customer_info WHERE customer_id = '{message.text}'")
            cur.execute(f"SELECT COUNT(*) FROM customer_info WHERE customer_id = '{message.text}'")
            det = int(cur.fetchone()[0])
            if det>0:
                await state.set_state(StatesOpDB.NONE)
                cur.execute(f"SELECT(customer_fio,phone_number,mail) FROM customer_info WHERE customer_id = {message.text} ORDER BY customer_num DESC LIMIT 1")
                temp = cur.fetchone()[0].split(',')
                cfio, phone, mail = temp[0][1:],temp[1],temp[2][:-1]
                await message.answer(f'ФИО: <code>{cfio}</code>\nНомер: <code>{phone}</code>\nПочта: <code>{mail}</code>')
            else:await message.answer('В базе данных <b>отсутвуют</b> данные о пользователе с таким ID, проверьте введенный ID')
        else:await message.answer('Вводимый ID пользователя должен состоять <b>только</b> из цифр!')
    else:await message.answer('ведено неверное количество аргументов! Должна быть одна строка содержащая ID пользователя')

async def set_order_info(message:Message,state:FSMContext):
    await state.set_state(StatesOpDB.NONE)
    if len(message.text.split('\n')) == 8:
        cid,oid,name,size,price,disc,date,adress = message.text.split('\n')
        if ' ' in cid:
            cid = cid.split()[0]
        if num_check(cid):
            if '/' not in oid and ' ' not in oid and not'\'' in oid and not '_' in oid and not '-' in oid and not '(' in oid and not ')' in oid:
                if len(date.split('.')) == 3:
                    day = date.split('.')[0]
                    month = date.split('.')[1]
                    year = date.split('.')[2]
                    if int(day)<=31 and int(month)<=12 and int(year)<=99:
                        db_protect(f"SELECT COUNT(*) FROM orders WHERE order_id ='{oid}'")
                        cur.execute(f"SELECT COUNT(*) FROM orders WHERE order_id ='{oid}'")
                        if int(cur.fetchone()[0]) == 0:
                            if not(',' in name or ',' in size or ',' in price or ',' in disc or ',' in adress):
                                if not'\'' in name and not'\'' in size and not'\'' in price and not'\'' in disc and not '\'' in adress:
                                    # db_protect(f"""INSERT INTO orders(customer_id,order_id,product_name,product_size,product_price,product_discount,order_date,adress)
                                    #             VALUES
                                    #             ({cid},'{oid}','{name}','{size}','{price}','{disc}','{month}-{day}-{year}','{adress}')""")
                                    cur.execute(f"""INSERT INTO orders(customer_id,order_id,product_name,product_size,product_price,product_discount,order_date,adress)
                                                VALUES 
                                                ({cid},'{oid}','{name}','{size}','{price}','{disc}','{month}-{day}-{year}','{adress}')""")
                                    conn.commit()
                                    await message.answer('Информация о заказе сохранена')
                                else:await message.answer('Поля не должны содержать символ(\')')
                            else:await message.answer('Неверный формат данных! Поля названий товаров, размеров, цен, скидок должны быть <b>без запятых и слешей</b> (,/).\nДопустимые символы: "+" "-" "=" "*"')
                        else:await message.answer('Заказ с введенным ID уже <b>существует</b> в базе данных')
                    else:await message.answer('Дата введена в неверном формате. Верный формат: ДД.ММ.ГГ')
                else:await message.answer('Дата введена в неверном формате. Верный формат: ДД.ММ.ГГ')
            else:await message.answer('ID заказа <b>не должен</b> содержать пробелы, " \' ", "_","-", скобки или слеши(/)')
        else:await message.answer('Вводимый ID пользователя должен состоять <b>только</b> из цифр!')
    else:await message.answer('Введено неверное количество аргументов! Должно быть 8 строк:\n1)ID клиента\n2)ID заказа\n3)Название товара\n4)Размер\n5)Стоимсть\n6)Скидка\n7)Дата (ДД.ММ.ГГ)\n8)Адрес')

async def show_order_info(message:Message,state:FSMContext):
    await state.set_state(StatesOpDB.NONE)
    db_protect(f"SELECT COUNT(*) FROM orders WHERE order_id = '{message.text}'")
    cur.execute(f"SELECT COUNT(*) FROM orders WHERE order_id = '{message.text}'")
    if int(cur.fetchone()[0]) >0:
        cur.execute(f"SELECT(customer_id,order_id,product_name,product_size,product_price,product_discount,order_date,adress) FROM orders WHERE order_id = '{message.text}'")
        temp = cur.fetchone()[0][1:-1]
        cid, oid, name, size, price, disc,date,adress = temp.split(',')
        await message.answer(f'Информация о заказе "<code>{oid}</code>":\n'
                             f'ID покупателя: <code>{cid}</code>\n'
                             f'Название товара(ов): <code>{name}</code>\n'
                             f'Размер: <code>{size}</code>\n'
                             f'Цена: <code>{price}</code>\n'
                             f'Скидка: <code>{disc}</code>\n'
                             f'Дата: <code>{date}</code>\n'
                             f'Адрес: <code>{adress}</code>\n')
    else:await message.answer(f'Заказ с введенным ID "{message.text}" отсутствует в базе даннх')

async def show_orders(message:Message,state:FSMContext):
    await state.set_state(StatesOpDB.NONE)
    if num_check(message.text):
        db_protect(f"SELECT COUNT(*) FROM orders WHERE customer_id = '{message.text}'")
        cur.execute(f"SELECT COUNT(*) FROM orders WHERE customer_id = '{message.text}'")
        num = int(cur.fetchone()[0])
        if num > 0:
            db_protect(f"SELECT (order_id,product_name) FROM orders WHERE customer_id = '{message.text}'")
            cur.execute(f"SELECT (order_id,product_name) FROM orders WHERE customer_id = '{message.text}'")
            msg_text = (f'Заказы пользователя <code>{message.text}</code>\n')
            for i in range(num):
                temp = cur.fetchone()[0][1:-1]

                pid,name = temp.split(',')
                msg_text +=f'{i+1}. ID заказа: <code>{pid}</code>\t Название: <code>{name}</code>\n'
            await message.answer(msg_text)
        else:await message.answer('Пользователь с таким ID не совершал заказов')
    else:await message.answer('Вводимый ID пользователя должен состоять <b>только</b> из цифр!')

async def state_setting(message:Message,state:FSMContext):
    await state.set_state(StatesOpDB.NONE)
    if message.text.count('-')==1 and not '\'' in message.text:
        temp = message.text.split('-')
        num, status = temp[0],temp[1]
        if not '_'in status:
            db_protect(f"SELECT COUNT(*) FROM orders WHERE order_id = '{num}'")
            cur.execute(f"SELECT COUNT(*) FROM orders WHERE order_id = '{num}'")
            if int(cur.fetchone()[0])==1:
                # db_protect(f"INSERT INTO order_state(order_id,order_status) VALUES ('{num}','{status}')")
                cur.execute(f"INSERT INTO order_state(order_id,order_status) VALUES ('{num}','{status}')")
                conn.commit()
                await message.answer('Статус заказа установлен')

            else:await message.answer(f'Заказ с ID "{num}" отсутствует в базе данных')
        else:await message.answer('Статус <b>не должен</b>содержать нижнее подчеркивание("_")')
    else:await message.answer(f'Введите ID и статус заказа через <b>ТИРЕ</b> (-). ОДИНАРНЫЕ КАВЫЧКИ (АПОСТРОФЫ) ЗАПРЕЩЕНЫ. Если есть трек-код, пропишите его в конце через пробел.\nПример:[ID]-[текст] [трек-код] (в квадратные скобки вставить нужное)')


