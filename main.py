import telebot
import random
import requests
from bs4 import BeautifulSoup as BS
from telebot import types

bot = telebot.TeleBot('<your token>')
# weather parser
r = requests.get('https://sinoptik.ua/погода-самара-100499099')
html = BS(r.content, 'html.parser')

for el in html.select('#content'):
    t_min = el.select('.temperature .min')[0].text
    t_max = el.select('.temperature .max')[0].text
    text = el.select('.wDescription .description')[0].text

# Welcome message (/start)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('img/Welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard main
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Мне повезёт?(0-100)")
    item2 = types.KeyboardButton("Хочу анекдот")
    item3 = types.KeyboardButton("Погода на сегодня")

    markup.add(item1, item2, item3)
    # Приветствие
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nДобро пожаловать❤️\nЯ - <b>креативный бот {1.first_name}</b>. \
                     Пока что я могу только нарандомить тебе число от 0 до 100 и рассказать парочку смешных анекдотов\
                     \n\n НО\n\nСкоро я буду делать много-много разных позезных вещей!".format(message.from_user,
                    bot.get_me()), parse_mode='html', reply_markup=markup)

# возможные ответы на твои действия
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Мне повезёт?(0-100)':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Погода на сегодня':
            bot.send_message(message.chat.id, "Привет, погода на сегодня:\n" +
                             t_min + ', ' + t_max + '\n' + text)

        elif message.text == 'Хочу анекдот':

            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Длинный и жизненный", callback_data='one')
            item2 = types.InlineKeyboardButton("Классический", callback_data='two')
            item3 = types.InlineKeyboardButton("Шорт - шутка", callback_data='three')
            item4 = types.InlineKeyboardButton("Один из лучший на планете", callback_data='four')

            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Выбери один из предложенных вариантов', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я немного глуповат, общайся со мной кнопочками, спасибо ❤️')

# Список анекдотов

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'one':
                bot.send_message(call.message.chat.id, 'Приезжает Путин в США. Обама устраивает в его честь роскошный прием. Путин интересуется: \n«На какие деньги банкет? Все-таки кризис!» \nОбама подводит его к окну: \n«Видите мост?» \n— «Ну».\n— «Он стоит 30 миллионов долларов. Мы провели тендер и нашлась компания, которая построила его за 25 миллионов. На разницу мы можем угостить русских друзей».\nПотом Обама приезжает в Россию. Еще более роскошный прием. Обама спрашивает: \n«На какие деньги?» \nПутин подводит его к окну: \n«Видите мост?» \n— «Нет». \n— «Во-о-от…»')
            elif call.data == 'two':
                bot.send_message(call.message.chat.id, 'Попали на необитаемый остров американец, немец и русский. Однажды прибило к острову бутылку, открыли они ее, а оттуда - джинн: \n- Вы меня освободили, я исполню по два ваших желания! \n- Мешок денег и домой! - сказал американец и исчез. \n- Кружку пива и домой! - сказал немец и был таков. \n- Хорошая была компания, ящик водки и всех обратно! - сказал русский.')
            elif call.data == 'three':
                bot.send_message(call.message.chat.id, 'На чемпионате мира по плаванию наш спортсмен занял третий шкафчик.')
            elif call.data == 'four':
                bot.send_message(call.message.chat.id, 'Поспорили как-то раз управляющие Нью-Йоркского и Московского Диснейлендов, чья комната страха страшнее. \nЗашел, значит, управляющий Московского в их комнату: скелеты всякие, привидения – в общем, ничего интересного. \nЗаходит теперь американец к нам, видит: длиннющий темный коридор, а в самом конце грузин на корточках сидит, в руке держит горящую свечку. \nГрузин: \n- Попа мыл? \n- Мыл. \nГрузин молча тушит свечку… ')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Внимание, А-НЕ-К-ДОТ",
                                  # reply_markup=None
                                  )



    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)