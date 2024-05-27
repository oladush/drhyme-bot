"""


"""

import os
import drhyme
import telebot
import logging
import pymorphy3
from drhyme import get_rhymes_score, rhymes_recount
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] [%(name)s]: %(message)s'
)

bot = telebot.TeleBot(token=TOKEN, colorful_logs=True)
morph = pymorphy3.MorphAnalyzer()


def to_gent(word):
    parsed = morph.parse(word)[0]
    return parsed.inflect({'gent'}).word

def gen_inline(words: list[str], orig: str) -> InlineKeyboardMarkup:
    '''
    generate inline keyboard with probably rhymes
    :param words: list of probably rhymes
    :return: markup object
    '''
    markup = InlineKeyboardMarkup()

    for word in words:
        markup.add(InlineKeyboardButton(text=f"💀 {word}", callback_data=f"{word}_{orig}".lower()))

    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "велкоме! я мейк рифмес. сендми эни ворд")


@bot.message_handler(func=lambda message: True)
def get_rhyme(message):
    try:
        rhymes = [(get_rhymes_score(word.lower()), word.lower()) for word in message.text.split()]
        logging.debug(f'Generated: {rhymes}')

        for rhymes_scores in rhymes:
            rhymes_, orig = rhymes_scores
            selected, _ = drhyme.internal.utils.get_max_score(rhymes_)
            others = [word for word in rhymes_ if word != selected]
            message_text = (f"{selected} 🤟 \n\nеще возможные варианты(проголосуй пж):")
            bot.reply_to(message, message_text, reply_markup=gen_inline(others, orig))

    except Exception as ex:
        bot.reply_to(message, 'разраб мудак ошибся гдето')
        logging.error(ex)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        rhyme, orig = call.data.split('_')
        logging.info(f"[*] updating rhyme {rhyme} ({orig})")
        bot.answer_callback_query(call.id, f"спасибо что выбрали {to_gent(rhyme)}. зачтется")
        rhymes_recount(rhyme, orig)
        logging.debug(f"Updated: {get_rhymes_score(orig)}")

    except Exception as ex:
        logging.error(ex)


if __name__ == "__main__":
    logging.info('[*] Starting bot pooling...')
    bot.polling()