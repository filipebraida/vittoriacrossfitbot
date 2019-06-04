from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from conf.settings import HTTP_CATS_URL, TELEGRAM_TOKEN

from bs4 import BeautifulSoup
from web import simple_get

def start(bot, update):
    response_message = "=^._.^="
    bot.send_message(
        chat_id=update.message.chat_id, text=response_message
    )


def http_cats(bot, update, args):
    bot.sendPhoto(
        chat_id=update.message.chat_id,
        photo=HTTP_CATS_URL + args[0]
    )


def wod(bot, update):
    print("Send msg")
    raw_html = simple_get('http://vittoriacrossfit.com/')
    html = BeautifulSoup(raw_html, 'html.parser')
    mydivs = html.findAll("a", {"class": "post__item__mais"})

    raw_html = simple_get(mydivs[0]['href'])
    html = BeautifulSoup(raw_html, 'html.parser')
    mydivs = html.findAll("section", {"class": "post-content"})

    response_message = mydivs[0].text
    print(response_message)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )

def unknown(bot, update):
    response_message = "Meow? =^._.^="
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


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
