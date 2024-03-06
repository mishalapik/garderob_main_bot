from aiogram import Bot,types
from aiogram.types import CallbackQuery,InputMediaPhoto,FSInputFile
from aiogram.fsm.context import FSMContext

from core.keyboards.inline import (mailing_kb,call_op_offer_kb,about_kb,shoes_or_clothes_kb,
                                   connect_kb,info_kb,backto_about_kb,backto_mailing_kb,backto_sizetables,backto_help_kb,help_kb)
from core.cannect.customer import askers
from core.data_base.db import conn,cur
from core.utils.statesform import StatesCustomer
from core.cannect.operator import waiting_for_reply
from core.data_base.orders import db_shut_protect,db_protect
from core.cannect.customer import askers
async def about(call:CallbackQuery,bot:Bot):
    await  call.message.edit_text(text='О магазине',reply_markup=about_kb)
    # await call.message.answer('О магазине',reply_markup=about_kb)
    # await bot.send_message(chat_id = call.from_user.id,text = 'Тут типа тескст о нас вот мы молодцы '
    #                                                           'сделали таокй крутой магазин покупайте нашу одежду',reply_markup=about_kb)
    await call.answer()
async def back_to_info_kb(call:CallbackQuery):
    await call.message.edit_text(text='Выберите вариант с помощью кнопок ниже:',reply_markup=info_kb)
async def about_us(call:CallbackQuery):
    await call.message.edit_text('Мы «<a href = "https://t.me/garderob_club1">Гардероб.club</a>». Как никто другой мы знаем, '
                              'насколько важно не только следить за трендами, но и находить в них себя.'
                              ' Мы - молодая и динамично развивающаяся компания, предоставляющая широкий выбор оригинальной, '
                              'брендовой одежды и обуви. Наша команда считает, что одежда - это состояние души, это способ самовыражения.'
                              ' Это то, что нас объединяет.'
                              ' Мы хотим помочь Вам создать свой уникальный стиль, выразить то, что внутри каждого из нас через одежду и обувь,'
                              ' а также обновить Ваш гардероб с нашей помощью!'
                              ' Приобретайте вещи, следите за новостями и становитесь частью нашего комьюнити!',reply_markup=backto_about_kb)

    await call.answer()
async def about_delivery(call:CallbackQuery):
    await call.message.edit_text('Доставка бесплатная и осуществляется во все уголки стран СНГ.'
                              ' Ее сроки - ориентировочно 21 день. '
                              'Сроки доставки товара могут измениться в зависимости от региона.'
                              ' Товар доставляется к Вам из Poizon, 1688, а также из Европы и США. Доставка осуществляется с помощью:\n\n'
                              '- Почта России (в отделение).\n- Курьер EMS.\n- СДЭК.\n\nТакже есть возможность отслеживать заказ по трек-номеру. '
                              'Зайдите в меню бота "Мои заказы" и он Вам сообщит статус заказа и трек-номер посылки.'
                              ' Информация о появлении трек-номера товара будет доступна после регистрации товара на границе.',reply_markup=backto_about_kb)

    await call.answer()
async def about_return(call:CallbackQuery):
    await call.message.edit_text('Возврат оформляется за наш счёт в течении 14 дней после получения заказа. Просим Вас убедиться в том, что товар сохранил свой первоначальный вид, включая упаковку производителя и сопутствующие ярлыки! '
                              'Возврат денежных средств осуществляется в течении 3-5 рабочий дней с момента получения нами посылки обратно. Каждый случай возврата рассматривается в индивидуальном порядке. '
                              '\n *Возврат за счёт нашей компании возможем в том случае, если пришёл товар ненадлежащего качества/брак '
                              '\n **Случаи, когда товар Вам не подошёл либо же Вы выбрали товар неподходящего размера, оплачиваются клиентом. Требуется оплатить отправку обратно через почтовую службу. При этом возвращается лишь часть стоимости товара.',reply_markup=backto_about_kb)

    await call.answer()


async def requisites(call:CallbackQuery, bot:Bot):
    await call.message.edit_text(text='Реквизиты компании <a href = "https://t.me/garderob_club1">Гардероб.club</a>:\n\nИП Трифонов Геннадий Александрович\n\nОГРНИП 323745600129361\n\nИНН 745307345383',
                                 reply_markup=backto_about_kb)

    await call.answer()

async def backto_about(call:CallbackQuery):
    await call.message.edit_text(text = 'О магазине',reply_markup=about_kb)

async def mailing(call:CallbackQuery, bot:Bot):
    await call.message.edit_text(text='Выберите вариант с помощью кнопок ниже:',reply_markup=mailing_kb)
    # await bot.send_message(chat_id = call.from_user.id,text='Выберите вариант с помощью кнопок ниже:',
    #                      reply_markup=mailing_kb)
    await call.answer()


async def ask_a_question(call:CallbackQuery,state:FSMContext):
    limit = 3
    if waiting_for_reply.count(call.from_user.id) < limit:

        await call.message.edit_text('Опишите свой вопрос (в одном сообщении, оператор <b>не видит</b> стикеры и голосовые сообщения от Вас):',reply_markup=None)
        waiting_for_reply.append(call.from_user.id)
        await call.answer()

        await state.set_state(StatesCustomer.ASKING_QUESTION)
    else:await call.message.edit_text(f'Вы уже оставили {limit} вопроса. Подождите пока на них ответит оператор')

async def mailing_check(call:CallbackQuery,bot:Bot):
    db_protect(f"""SELECT mailing_state FROM mailing
                    WHERE user_id = {call.from_user.id}
                    ORDER BY ser_num DESC
                    LIMIT 1""")
    cur.execute(f"""SELECT mailing_state FROM mailing
                    WHERE user_id = {call.from_user.id}
                    ORDER BY ser_num DESC
                    LIMIT 1""")
    res = str(cur.fetchone()[0])
    if res =='True':
        await call.message.edit_text('На вашем аккаунте рассылка <b>включена</b>',reply_markup=backto_mailing_kb)
    else:
        await call.message.edit_text('На вашем аккаунте рассылка <b>выключена</b>',reply_markup=backto_mailing_kb)
    await call.answer()
async def mailing_on(call:CallbackQuery,bot:Bot):
    await call.message.edit_text('Рассылка включена, теперь Вы получаете все важные новости о предстоящих событиях и скидках!',reply_markup=backto_mailing_kb)
    db_shut_protect()
    cur.execute(f"INSERT INTO mailing(user_id,mailing_state) VALUES ({call.from_user.id},true)")

    await call.answer()
    conn.commit()



async def mailing_off(call:CallbackQuery,bot:Bot):
    await call.message.edit_text('Рассылка выключена :(',reply_markup=backto_mailing_kb)
    db_shut_protect()
    cur.execute(f"INSERT INTO mailing(user_id,mailing_state) VALUES ({call.from_user.id},false)")
    await call.answer()
    conn.commit()




async def call_op_to_continue(call:CallbackQuery,bot:Bot):
    await call.message.edit_text('Для продолжения заказа свяжитесь с оператором',reply_markup=call_op_offer_kb)
    await call.answer()


async def size_tables(call:CallbackQuery,bot:Bot):

    await call.message.edit_text(text='Выберите вариант с помощью кнопок ниже:',reply_markup=shoes_or_clothes_kb)
    # await call.message.answer('Выберите вариант:',reply_markup=shoes_or_clothes_kb)
    # await bot.send_photo(chat_id = call.from_user.id,photo='AgACAgIAAxkBAAIWt2VDfbaAJyIOrSuMCjtuYJA4D_lOAAJO0TEbB1YZSsz-uPYLrlK7AQADAgADeAADMwQ',caption='Таблица размеров')
    await call.answer()

async def shoes_male_table(call:CallbackQuery,bot:Bot):
    # photo = InputMediaPhoto(type='photo',media=FSInputFile(r'C:\Users\Mikhail\PycharmProjects\garderob_bot\core\media\shoes.jpg'))

    await bot.send_photo(chat_id=call.from_user.id,photo = FSInputFile('core/media/male_shoes_table.png'),reply_markup=backto_sizetables)
    # await bot.send_photo(chat_id=call.from_user.id,
    #                      photo=r'https://sun9-31.userapi.com/impg/VnItjis2k6HxUfgAd_JDLD1gXwj5MxdfMBP_JA/ZO7GyQg9LSo.jpg?size=1500x1600&quality=96&sign=9d4461846486ad9561a6f6fb4e3c1f8f&type=album',
    #                      caption='Таблица размеров обуви',reply_markup=backto_sizetables)
    await call.answer()

async def shoes_female_table(call:CallbackQuery,bot:Bot):
    # photo = InputMediaPhoto(type='photo',media=FSInputFile(r'C:\Users\Mikhail\PycharmProjects\garderob_bot\core\media\shoes.jpg'))

    await bot.send_photo(chat_id=call.from_user.id,photo = FSInputFile('core/media/female_shoes_table.png'),reply_markup=backto_sizetables)
    # await bot.send_photo(chat_id=call.from_user.id,
    #                      photo=r'https://sun9-31.userapi.com/impg/VnItjis2k6HxUfgAd_JDLD1gXwj5MxdfMBP_JA/ZO7GyQg9LSo.jpg?size=1500x1600&quality=96&sign=9d4461846486ad9561a6f6fb4e3c1f8f&type=album',
    #                      caption='Таблица размеров обуви',reply_markup=backto_sizetables)
    await call.answer()
async def clothes_table(call:CallbackQuery,bot:Bot):

    await bot.send_photo(chat_id=call.from_user.id,
                         photo='https://sun9-6.userapi.com/impg/XuevzCCnAHKx_zyLrsNyIZqFlF4hNG0M73iO7Q/sguUQoiz6Ag.jpg?size=1500x1500&quality=96&sign=9c58d9133e92afe43711730ea2777792&type=album',
                         # photo='AgACAgIAAxkBAAIY02VFRBr9GR0CU7UVbDm90L32jlnkAAK-1TEbiu8pSsoiVskV-lzEAQADAgADeQADMwQ',
                         caption='Таблица размеров верхней одежды',reply_markup=backto_sizetables)
    await call.answer()

async def pants_table(call:CallbackQuery,bot:Bot):
    await bot.send_photo(chat_id=call.from_user.id,
                         photo='https://sun9-18.userapi.com/impg/u31Tt4ZKpzdONpEAZyPjnQ6FYvhwLDx2eBvaSQ/n-fTdpPajXI.jpg?size=1500x1500&quality=96&sign=60a17a0636056da9ecdf337bc98d330c&type=album',
                         caption='Таблица размеров брючных изделий', reply_markup=backto_sizetables)
    await call.answer()
async def backto_size_tables(call:CallbackQuery):
    await call.message.delete()

    await call.answer()


async def ask_or_dialog(call:CallbackQuery):
    await call.message.edit_text('Выберите вариант с помощью кнопок ниже:',reply_markup=connect_kb)
    await call.answer()

async def working_time(call:CallbackQuery):
    await call.message.edit_text('Время работы магазина с 8:00 до 21:00 по МСК в будние дни, в выходные с 9:00 до 20:00 по МСК.',reply_markup=backto_help_kb)
    await call.answer()
async  def learn_sizes(call:CallbackQuery):
    await call.message.edit_text('<b>КАК УЗНАТЬ НУЖНЫЙ РАЗМЕР?</b>\n\n'
                              'Отнеситесь к выбору размера очень внимательно! '
                              'Для более точного определения размера обуви или одежды '
                              'Вы можете воспользоваться размерной сеткой в разделе нашего бота <b>"Таблицы размеров"</b> в меню <b>"Информация".</b> '
                              'При выборе размера обуви лучше всего использовать линейку и измерить стопу в сантиметрах и соотносить полученные цифры с таблицей размеров обуви. '
                              'При выборе одежды воспользуйтесь линейкой-сантиметром для измерения и также соотносите полученные цифры с таблицей размеров одежды.\n\n'
                              'При возникновении проблем в выборе нужного размера Вы всегда можете обратиться к нашим операторам. Помните, что при выборе неправильного размера мы не сможем оформить возврат.',reply_markup=backto_help_kb)
    await call.answer()

async def brands_guarantee(call:CallbackQuery):
    await call.message.edit_text('<b>БРЕНДЫ:</b>\n\nНаш Гардероб предоставляет обширный ассортимент товаров и различных брендов, таких как:'
                              ' Nike, Adidas, New Balance, PUMA, Reebok, Vans, Converse, Caterpillar и т.д \n\n<b>ГАРАНТИИ КАЧЕСТВА:</b>\n\n'
                              'Мы гарантируем, что наш Гардероб предоставляет только оригинальные товары от именитых брендов. '
                              'Товар доставляется от официальных поставщиков из-за границы. '
                              'При получении товара с <a href = "https://t.me/garderob_club1/55">Poizon</a> Вы получаете сертификат соответствия для определения оригинальности. '
                              'Также следите за каналом "<a href = "https://t.me/garderob_club1">Гардероб.club</a>", на нём мы делаем регулярные распаковки и обзоры культовых '
                              'пар обуви и одежды. Если Вам по каким-то причинам пришла реплика или подделка заказанная через '
                              'наш магазин, то мы вернём Вам деньги.',reply_markup=backto_help_kb)
    await call.answer()
async def delivery_return(call:CallbackQuery):
    await call.message.edit_text('<b>ДОСТАВКА:</b> \n\nДоставка бесплатная и осуществляется во все уголки стран СНГ.'
                              ' Ее сроки - ориентировочно 21 день. Сроки доставки товара могут измениться в зависимости от региона. '
                              'Товар доставляется к Вам из Poizon, 1688, а также из Европы и США.\n\nДоставка осуществляется с помощью:\n\n'
                              '- Почта России (в отделение).\n- Курьер EMS. \n- СДЭК. \nТакже есть возможность отслеживать заказ по трек-номеру. '
                              'Зайдите в меню бота "Мои заказы" и он Вам сообщит статус заказа и трек-номер посылки. '
                              'Информация о появлении трек-номера товара будет доступна после регистрации товара на границе. \n\n<b>ВОЗВРАТ:</b>\n\n'
                              'Возврат оформляется за наш счёт в течении 14 дней после получения заказа. Просим Вас убедиться в том, что товар сохранил свой первоначальный вид, включая упаковку производителя и сопутствующие ярлыки!\n'
                              'Возврат денежных средств осуществляется в течении 3-5 рабочий дней с момента получения нами посылки обратно. Каждый случай возврата рассматривается в индивидуальном порядке.\n'
                              '\n *Возврат за счёт нашей компании возможем в том случае, если пришёл товар ненадлежащего качества/брак '
                              '\n **Случаи, когда товар Вам не подошёл либо же Вы выбрали товар неподходящего размера, оплачиваются клиентом. Требуется оплатить отправку обратно через почтовую службу. При этом возвращается лишь часть стоимости товара.'
                              '\n\n<b>ОБМЕН</b>:\n\nНаш Гардероб не предоставляет и не рассматривает '
                              'возможности обмена товаров на что-либо с доплатой или без.',reply_markup=backto_help_kb)
    await call.answer()
async def discounts_bounus(call:CallbackQuery):
    await call.message.edit_text('<b>АКЦИИ, СКИДКИ:</b> \n\nВ нашем Гардеробе присутствуют сезонные скидки и акции на определённые категории товаров.  '
                              'А также акции во время праздников и ивентов. '
                              'Об актуальных акциях и скидках Вы можете узнать в канале "<a href = "https://t.me/garderob_club2">Гардероб.shop</a>" \n\n<b>БОНУСЫ:</b>\n\n'
                              'В будущем планируется внедрение системы лояльности и бонусов для Вас,'
                              ' поэтому следите за нашими новостями и мы Вас обязательно порадуем лучшими предложениями!',reply_markup=backto_help_kb)
    await call.answer()
async def prices_payments(call:CallbackQuery):
    await call.message.edit_text('<b>СТОИМОСТЬ:</b>\n\nЦена товара находится на карточке в каталоге канала "<a href = "https://t.me/garderob_club2">Гардероб.shop</a>". '
                              'Цена представлена в виде "*Цена от" так как корректировка цен происходит периодически, примерно раз в 2-3 дня.\n\n<b>СПОСОБЫ ОПЛАТЫ:</b>\n\n'
                              'Оплата товара производится с помощью СБП, при оплате оператор высылает Вам QR-код, по нему нужно перейти и ввести стоимость товара, озвученную оператором.'
                              ' Если невозможно оплатить QR-кодом, то существует альтернативный вариант оплаты товара с помощью банковской карты. Оператор присылает в чат ссылку на оплату через платёжный шлюз.',reply_markup=backto_help_kb,parse_mode='HTML')
    await call.answer()


async def backto_FAQ(call:CallbackQuery):
    await call.message.edit_text('Выберите вариант с помощью кнопок ниже:',reply_markup=help_kb)


async def decline_offer(call:CallbackQuery):
    await call.message.edit_text('Пришлите желаемую товарную карточку-сообщение из канала <a href = "https://t.me/garderob_club2">Гардероб.shop</a> для оформления заказа')
    await  call.answer()


async def terms_of_use(call:CallbackQuery,bot:Bot):
    fn = r'core/media/Пользовательское соглашение.docx'
    # fn = r'core\media\Пользовательское соглашение.docx'
    terms = FSInputFile(fn)
    await bot.send_document(chat_id=call.from_user.id,document=terms,caption='Пользовательское соглашение')
    await call.answer()
