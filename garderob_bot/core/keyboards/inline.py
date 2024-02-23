from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


info_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'О магазине',callback_data='about')],
    [InlineKeyboardButton(text = 'Канал Гардероб.club',url='https://t.me/garderob_club1')],
    [InlineKeyboardButton(text = 'Рассылка',callback_data='mailing')],
    [InlineKeyboardButton(text = 'Таблица размеров',callback_data='size_tables')],
    [InlineKeyboardButton(text = 'Пользовательское соглашение',callback_data='terms_of_use')]
])

about_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='О нас',callback_data='about_us')],
    [InlineKeyboardButton(text='Доставка',callback_data='about_delivery')],
    [InlineKeyboardButton(text='Возврат',callback_data='about_return')],
    [InlineKeyboardButton(text='Реквизиты',callback_data='requisites')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_info_kb')]
])
backto_about_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад',callback_data='backto_about_kb')]])
mailing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Получать рассылку',callback_data='start_mailing')],
    [InlineKeyboardButton(text = 'Отказаться от рассылки',callback_data='stop_mailing')],
    [InlineKeyboardButton(text = 'Проверить статус рассылки',callback_data='check_mailing')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_info_kb')]
])
backto_mailing_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад',callback_data='mailing')]])

help_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Стоимость и способы оплаты',callback_data='prices_payments')],
    [InlineKeyboardButton(text='Акции, Скидки, Бонусы',callback_data='discounts_bounus')],
    [InlineKeyboardButton(text='Доставка, возврат, обмен',callback_data='delivery_return')],
    [InlineKeyboardButton(text='Бренды и гарантии качества',callback_data='brands_guarantee')],
    [InlineKeyboardButton(text='Как узнать нужный размер',callback_data='learn_sizes')],
    [InlineKeyboardButton(text='Время работы магазина',callback_data='working_time')],
    [InlineKeyboardButton(text='Задать вопрос',callback_data='ask')]

])
backto_help_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад',callback_data='backto_help_kb')]])
connect_kb = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text = 'Оставить сообщение',callback_data='ask_a_question')],
    [InlineKeyboardButton(text = 'Связаться с оператором',callback_data='connect_to_operator')],
    [InlineKeyboardButton(text='Назад',callback_data='backto_help_kb')]
])

ask_one_question_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Оставить сообщение',callback_data='ask_a_question')]])

pre_offer_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Да, хочу заказать товар',callback_data='confirm_offer')],
    [InlineKeyboardButton(text = 'Назад',callback_data='decline_offer')]
    # [InlineKeyboardButton(text = 'отказаться',callback_data='decline_offer')]
])

call_op_offer_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Связаться с оператором',callback_data='connect_to_operator')]])

# to_order_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Связаться с оператором',callback_data='connect_to_operator')],
#     [InlineKeyboardButton(text='Ассортимент',url='https://t.me/garderob_club1')]
# ])

shoes_or_clothes_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Таблица размеров верхней одежды',callback_data='clothes_table')],
    [InlineKeyboardButton(text='Таблица размеров обуви',callback_data='shoes_table')],
    [InlineKeyboardButton(text='Таблица размеров брючных изделий',callback_data='pants_table')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_info_kb')]
])
backto_sizetables = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад',callback_data='backto_size_tables')]])
channelbtn_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перейти в канал',url='https://t.me/garderob_club2')]
])

backto_help_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад',callback_data='backto_help_kb')]])

