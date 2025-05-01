
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PROMO_FILE = "promo_codes.txt"
if not os.path.exists(PROMO_FILE):
    with open(PROMO_FILE, "w") as f:
        f.write("76X123EXAMPLE\n")

def get_next_promo():
    with open(PROMO_FILE, "r") as f:
        codes = f.read().splitlines()
    if not codes:
        return None
    code = codes[0]
    with open(PROMO_FILE, "w") as f:
        f.write("\n".join(codes[1:]))
    return code

WELCOME_TEXT = (
    "Добрый день!\n\n"
    "Чтобы получить бонусы, подпишитесь на наш телеграм-канал 👉 [перейти](https://t.me/+uHVf9lRmaCpmYWYy)\n\n"
    "В канале:\n"
    "— ⚡ выгодные предложения по подключению интернета\n"
    "— 🛠️ технические лайфхаки\n"
    "— 🛰️ информация о сбоях\n"
    "— 🎉 розыгрыши с крутыми призами\n"
    "— 🐾 и, конечно, мемы!\n\n"
    "После подписки нажмите кнопку ниже, чтобы получить свои бонусы 🎁"
)

BONUS_TEXT_TEMPLATE = (
    "Ваши бонусы:\n\n"
    "1. Подписка на Яндекс.Плюс на 2 месяца для новых пользователей! С подпиской вам будут доступны сервисы Кинопоиск, Яндекс.Музыка, а также вы сможете копить баллы и тратить их на такси или доставку еды и продуктов.\n"
    "Активировать промокод нужно в течение месяца.\n"
    "\n"
    "*{yandex_code}*\n"
    "\n"
    "2. Месяц бесплатной PRO подписки на сервис VPNTYPE. Это VPN-сервис, который поддерживает все современные протоколы и обеспечивает максимальную защиту данных на всех устройствах. Промокод DOMATELECOM активировать можно через бота @vpntypebot\n"
    "\n"
    "Промокод DOMATELECOM даст вам месяц БЕСПЛАТНОЙ премиум-подписки на сервис VPNTYPE.\n"
    "Активировать можно через бота @vpntypebot"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Получить бонус", callback_data="get_bonus")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    promo = get_next_promo()
    if not promo:
        await query.edit_message_text("Извините, промокоды закончились 😿")
        return

    bonus_text = BONUS_TEXT_TEMPLATE.format(yandex_code=promo)
    await query.edit_message_text(bonus_text, parse_mode='Markdown')

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
