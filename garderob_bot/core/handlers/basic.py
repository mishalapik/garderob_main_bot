from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import psycopg2
from core.keyboards.reply import main_menu_kb
from core.keyboards.inline import info_kb,connect_kb,channelbtn_kb,help_kb
from core.data_base.db import cur,conn
from core.utils.statesform import forward
from core.config.data import admin_id
from core.data_base.orders import db_shut_protect





async def get_start(message:Message,bot:Bot):
    await message.answer(text = f'На связи Гардероб.club! Приветствую, {message.from_user.first_name}, выбери интересующий тебя раздел.',reply_markup=main_menu_kb)
    db_shut_protect()
    try:
        global cur,conn
        cur.execute(f"SELECT COUNT(*) FROM mailing WHERE user_id = {message.from_user.id}")
    except psycopg2.InterfaceError:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM mailing WHERE user_id = {message.from_user.id}")

    except psycopg2.InterfaceError as exc:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM mailing WHERE user_id = {message.from_user.id}")
    except psycopg2.OperationalError:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM mailing WHERE user_id = {message.from_user.id}")
    except psycopg2.errors.InFailedSqlTransaction:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM mailing WHERE user_id = {message.from_user.id}")
    det = int(cur.fetchone()[0])

    if det == 0:
        cur.execute(f"INSERT INTO mailing(user_id,mailing_state) VALUES ({int(message.from_user.id)},true)")
        conn.commit()

async def info(message:Message,bot:Bot):
    await message.answer('Выберите вариант с помощью кнопок ниже:',reply_markup=info_kb)

async def app_temp(message:Message,bot:Bot):
    await message.answer('Для оформления заказа перешлите из канала '
                         '<a href = "https://t.me/garderob_club2">Гардероб.shop </a>сообщение с нужным '
                         'Вам товаром, бот автоматически определит выбранный Вами товар и свяжет с оператором.\nО гарантиях качества вы можете прочитать в разделе "Бренды и гарантии качества" основного меню "FAQ".',reply_markup=channelbtn_kb)

async def connect(message:Message,bot:Bot):
    await message.answer('Выберите вариант:',reply_markup=help_kb)


async def orders(message:Message):

    try:
        global cur,conn
        cur.execute(f"SELECT COUNT(*) FROM orders WHERE customer_id = {message.from_user.id}")
    except psycopg2.ProgrammingError as exc:
        conn.rollback()
        cur.execute(f"SELECT COUNT(*) FROM orders WHERE customer_id = {message.from_user.id}")
    except psycopg2.InterfaceError as exc:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM orders WHERE customer_id = {message.from_user.id}")
    except psycopg2.OperationalError:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM orders WHERE customer_id = {message.from_user.id}")
    except psycopg2.errors.InFailedSqlTransaction:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM orders WHERE customer_id = {message.from_user.id}")
    det = int(cur.fetchone()[0])
    if det == 0:
        await message.answer('К сожалению, у Вас пока нет активных заказов. Вы можете выбрать для себя товар перейдя по кнопке <b>"Заказать"</b> в главном меню бота.')
    else:
        msg = ''
        await message.answer(f'Ваши заказы:')
        cur.execute(f"SELECT (product_name,order_id) FROM orders WHERE customer_id = {message.from_user.id}")
        for i in range(det):
            name,oid = cur.fetchone()[0][1:-1].split(",")
            msg+=f"{1+i}. {name}, проверить статус - /check_{oid}\n"
        await message.answer(msg)

async def state_check(message:Message):
    num = message.text.split('_')[1]
    try:
        global cur,conn
        cur.execute(f"SELECT COUNT(*) FROM order_state WHERE order_id = '{num}'")
    except psycopg2.ProgrammingError as exc:
        conn.rollback()
        cur.execute(f"SELECT COUNT(*) FROM order_state WHERE order_id = '{num}'")
    except psycopg2.InterfaceError as exc:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM order_state WHERE order_id = '{num}'")
    except psycopg2.OperationalError:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM order_state WHERE order_id = '{num}'")
    except psycopg2.errors.InFailedSqlTransaction:
        conn = psycopg2.connect(database='garderob_main_db', user='postgres', host='localhost', port='5432',
                                password='yesterday')
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM order_state WHERE order_id = '{num}'")
    if int(cur.fetchone()[0])==1:
        cur.execute(f"SELECT order_status FROM order_state WHERE order_id = '{num}' ORDER BY order_num DESC LIMIT 1")
        temp = cur.fetchone()
        await message.answer(f'Статус заказа:{temp[0]}')
    else:await message.answer('Статус такого заказа не найден. Пожалуйста, проверьте позже или обратитесь к оператору.')
    #
# async def main_menu(message:Message,bot:Bot):
#     await message.answer('меню',reply_markup=main_menu_kb)