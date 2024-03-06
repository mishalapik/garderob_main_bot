from aiogram import Bot,Dispatcher,F
from aiogram.types import Message
import asyncio
import logging
from core.config.data import operator
from core.config.data import admin_id,token

from core.handlers.basic import get_start,info,app_temp,connect,orders,state_check

from core.handlers.callback import (about,requisites,mailing,ask_a_question,mailing_on,mailing_off,mailing_check,call_op_to_continue,about_us,about_return,
                                    about_delivery,size_tables,shoes_male_table,shoes_female_table,clothes_table,ask_or_dialog,working_time,learn_sizes,brands_guarantee,
                                    delivery_return,discounts_bounus,prices_payments,back_to_info_kb,backto_about,backto_size_tables,backto_FAQ,pants_table,
                                    decline_offer,terms_of_use)

from core.cannect.customer import send_question,cust_chat,confirm_offer

from core.cannect.operator import (answer_toa_question,dyalog_start_or_drop,op_online,op_offline,
                                   accept_conv,op_msg_reply,close_conv,begin_mailing,get_mailing_text,
                                   get_mailing_pic,send_mailing,insert_cust_info,get_cust_info,add_order,get_order,
                                   get_orders,set_status,op_pic_reply,anspic,send_msg)
from core.utils.statesform import StepsMailing,forward,StatesCustomer,StatesOpDB

from core.data_base.orders import set_cust_info,show_cust_info,set_order_info,show_order_info,show_orders,state_setting

from core.data_base.db import data_base_copy,show_ops,show_gods,show_el_ops,add_el_op,add_operator,remove_operator,remove_el_op,conn,clear_data_base
async def bot_started(bot:Bot):
    await bot.send_message(chat_id=admin_id,text = 'bot started')
    # await bot.send_message(chat_id=operator, text='bot started')
async def bot_closed(bot:Bot):
    await bot.send_message(chat_id=admin_id,text = 'bot closed')
    # await bot.send_message(chat_id=operator, text='bot closed')
    conn.commit()

async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    # dp.message.register(main_menu,F.text == '/menu')
    dp.message.register(get_start,F.text == '/start')
    dp.message.register(info,F.text == 'Информация')
    dp.message.register(app_temp,F.text == "Заказать")
    dp.message.register(connect,F.text == 'FAQ')
    dp.message.register(orders,F.text =='Мои заказы')
    dp.message.register(answer_toa_question, F.text.startswith('/answer'))
    dp.message.register(op_online, F.text == '/on')
    dp.message.register(op_offline,F.text == '/off')
    dp.message.register(accept_conv,F.text == '/accept')
    dp.message.register(begin_mailing,F.text == '/mailing')
    dp.message.register(send_mailing,F.text == '/send')
    dp.message.register(insert_cust_info,F.text =='/setinfo')
    dp.message.register(get_cust_info,F.text == '/getinfo')
    dp.message.register(data_base_copy,F.text == '/GETDATABASE')
    dp.message.register(clear_data_base,F.text =='/CLEARDATABASE')
    dp.message.register(add_order,F.text == '/addorder')
    dp.message.register(get_order,F.text == '/getorder')
    dp.message.register(get_orders,F.text =='/getorders')
    dp.message.register(set_status,F.text == '/setstatus')
    dp.message.register(show_gods,F.text =='/showgods')
    dp.message.register(show_ops,F.text == '/showops')
    dp.message.register(show_el_ops,F.text=='/showelite')
    dp.message.register(send_msg,F.text.startswith('/sendmsg'))
    dp.message.register(remove_operator,F.text.startswith('/removeop'))
    dp.message.register(remove_el_op,F.text.startswith('/removeelite'))
    dp.message.register(add_operator,F.text.startswith('/addop'))
    dp.message.register(add_el_op,F.text.startswith('/addelite'))
    dp.message.register(op_msg_reply,F.text.startswith('/reply'))
    dp.message.register(state_check,F.text.startswith('/check'))
    dp.message.register(close_conv,F.text.startswith('/finish'))
    dp.message.register(anspic,F.caption.split()[0]=='/answerpic')

    dp.message.register(set_cust_info,StatesOpDB.INSERT_INFO)
    dp.message.register(show_cust_info,StatesOpDB.GET_INFO)
    dp.message.register(set_order_info,StatesOpDB.ADD_ORDER)
    dp.message.register(show_order_info,StatesOpDB.GET_ORDER)
    dp.message.register(show_orders,StatesOpDB.GET_ORDERS)
    dp.message.register(state_setting,StatesOpDB.SET_ORDER_STATE)

    dp.message.register(send_question,StatesCustomer.ASKING_QUESTION)
    dp.message.register(get_mailing_text,StepsMailing.INSERT_TEXT)
    dp.message.register(get_mailing_pic,StepsMailing.INSERT_MEDIA)

    dp.callback_query.register(terms_of_use,F.data=='terms_of_use')
    dp.callback_query.register(decline_offer,F.data =='decline_offer')
    dp.callback_query.register(pants_table,F.data == 'pants_table')
    dp.callback_query.register(backto_FAQ,F.data=='backto_help_kb')
    dp.callback_query.register(backto_size_tables,F.data == 'backto_size_tables')
    dp.callback_query.register(backto_about,F.data == 'backto_about_kb')
    dp.callback_query.register(back_to_info_kb,F.data == 'back_to_info_kb')
    dp.callback_query.register(prices_payments,F.data == 'prices_payments')
    dp.callback_query.register(discounts_bounus,F.data == 'discounts_bounus')
    dp.callback_query.register(delivery_return,F.data == 'delivery_return')
    dp.callback_query.register(brands_guarantee,F.data == 'brands_guarantee')
    dp.callback_query.register(learn_sizes,F.data=='learn_sizes')
    dp.callback_query.register(working_time,F.data=='working_time')
    dp.callback_query.register(ask_or_dialog,F.data == 'ask')
    dp.callback_query.register(shoes_male_table,F.data == 'shoes_male_table')
    dp.callback_query.register(shoes_female_table, F.data == 'shoes_female_table')
    dp.callback_query.register(clothes_table, F.data == 'clothes_table')
    dp.callback_query.register(size_tables,F.data == 'size_tables')
    dp.callback_query.register(dyalog_start_or_drop,F.data == 'connect_to_operator')
    dp.callback_query.register(about, F.data == 'about')
    dp.callback_query.register(mailing, F.data == 'mailing')
    dp.callback_query.register(requisites, F.data =='requisites')
    dp.callback_query.register(about_us,F.data=='about_us')
    dp.callback_query.register(about_delivery,F.data == 'about_delivery')
    dp.callback_query.register(about_return,F.data == 'about_return')
    dp.callback_query.register(ask_a_question,F.data == 'ask_a_question')
    dp.callback_query.register(mailing_on,F.data =='start_mailing')
    dp.callback_query.register(mailing_off,F.data == 'stop_mailing')
    dp.callback_query.register(mailing_check, F.data == 'check_mailing')
    dp.callback_query.register(call_op_to_continue,F.data == 'confirm_offer')

    # dp.message.register(op_pic_reply,F.photo)
    dp.message.register(confirm_offer,F.photo)
    dp.message.register(cust_chat,F.text)

    dp.startup.register(bot_started)
    dp.shutdown.register(bot_closed)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())