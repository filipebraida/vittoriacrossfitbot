from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from conf.settings import HTTP_CATS_URL, TELEGRAM_TOKEN

from bs4 import BeautifulSoup
from web import simple_get


def send_msg(bot, update, message):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )

def start(bot, update):
    message = 'Bem vindo ao Crossfit Vittoria Bot.\n' \
    'O bot foi desenvolvido por Filipe Braida.\n'
    'Use o comando \\help para saber as funcionalidades.'
    
    send_msg(bot, update, message)


def http_cats(bot, update, args):
    bot.sendPhoto(
        chat_id=update.message.chat_id,
        photo=HTTP_CATS_URL + args[0]
    )

def help_reply() -> str:
    reply = 'Comandos do Vittoria Crossfit Bot:\n\n' \
            '/wod - informa o wod do dia.' 
    return reply

def help(bot, update):    
	send_msg(bot, update, help_reply())

def work_of_day() -> str:
	raw_html = simple_get('http://vittoriacrossfit.com/')
	html = BeautifulSoup(raw_html, 'html.parser')
	mydivs = html.findAll("a", {"class": "post__item__mais"})

	raw_html = simple_get(mydivs[0]['href'])
	html = BeautifulSoup(raw_html, 'html.parser')
	mydivs = html.findAll("section", {"class": "post-content"})

	return mydivs[0].text

def wod(bot, update):
    print('-- Command \\wod by ' + str(update.message.chat_id))
    send_msg(bot, update, work_of_day())

def unknown(bot, update):
    send_msg(bot, update, help_reply())

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('http', http_cats, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('wod', wod)
    )
    dispatcher.add_handler(
        CommandHandler('help', help)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
main()
