from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Заказать')],
    [KeyboardButton(text = 'Информация',)],
    [KeyboardButton(text = 'FAQ')],
    [KeyboardButton(text = 'Мои заказы')]
],resize_keyboard=True)

# op_kb = ReplyKeyboardMarkup(keyboard=[
#     []
# ])
