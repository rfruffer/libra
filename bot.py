from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request
from telegram import Bot
from telegram import Update
#from emoji import UNICODE_EMOJI
from telegram.ext import CallbackContext
import sys
import io

sys.stdout = io.open(sys.stdout.fileno(), 'w', encoding='utf8')

UNICODE_EMOJI = ['💋','👄','🔥','⚡','☄','️🌈','🍓','🌶','️🥕','🍆','💊','❤','️❌','⛔','📛','🚫','🔞','❗','💥','💝','💘','💖','💗','💓','💞','💕','🔴']

telegram_token = ''

def members(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    for member in update.message.new_chat_members:
        if is_emoji(member.first_name) or is_emoji(member.username):
            try:
                context.bot.kick_chat_member(chat_id,member.id)
                context.bot.delete_message(chat_id,update.message.message_id)
            except Exception as e:
                print(e)

def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if update.message.from_user.id == 1111:
        context.bot.delete_message(chat_id,update.message.message_id)

def is_emoji(s):
    count = 0
    for emoji in UNICODE_EMOJI:
        count += s.count(emoji)
        if count >= 2:
            return True
    return False

def main():
    print ("Запускаем бота...")
    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token=telegram_token,
        request=req
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )


    members_handler = MessageHandler(Filters.status_update.new_chat_members, members)
    message_handler = MessageHandler(Filters.status_update.left_chat_member, do_echo)

    updater.dispatcher.add_handler(members_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

    print ("Закончили работу...")

if __name__ == '__main__':
    main()
