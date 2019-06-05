from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from emoji import emojize

from bs4 import BeautifulSoup
from web import simple_get

from database import TelegramUser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData


def send_msg(bot, update, message):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )

def start(bot, update):
    message = 'Bem vindo ao Crossfit Vittoria Bot.\n' \
    'O bot foi desenvolvido por Filipe Braida.\n'
    'Use o comando \\help para saber as funcionalidades.'

    if not has_user(engine, update.message.from_user.id):
        insert_new_user_to_db(engine, update.message.from_user.id, update.message.from_user.full_name)
    
    send_msg(bot, update, message)

def init_db(uri):    
    sqlite_engine = create_engine(uri)
    sqlite_engine.execute("CREATE TABLE IF NOT EXISTS `telegram_users` ( `id` INTEGER, `name` TEXT, `active` INTEGER, PRIMARY KEY(`id`) )")
    return

def help_reply() -> str:
    icon = emojize(":information_source: ", use_aliases=True)
    text = icon + " Os seguintes comandos estão disponíveis:\n"

    commands = [["/wod", "Lista o wod do dia"],
               ["/liga", "Liga a notificação diária"],
               ["/desliga", "desliga a notificação diária"],
               ["/status", "Verifica o status do usuário"],
               ["/help", "Recebe essa mensagem"]
               ]

    for command in commands:
        text += command[0] + " " + command[1] + "\n"
    
    return text

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
    user = get_user(engine, update.message.chat_id)

    if user is None:
        insert_new_user_to_db(engine, update.message.from_user.id, update.message.from_user.full_name)

    print('-- Command \\wod by ' + str(user))
    send_msg(bot, update, work_of_day())

def unknown(bot, update):    
    send_msg(bot, update, "Comando desconhecido. Utilize o \\help")

def liga(bot, update):
    user = get_user(engine, update.message.chat_id)

    if user is None:
        insert_new_user_to_db(engine, update.message.from_user.id, update.message.from_user.full_name)

    send_msg(bot, update, user.msg_ativo())

def desliga(bot, update):
    user = get_user(engine, update.message.chat_id)

    if user is None:
        insert_new_user_to_db(engine, update.message.from_user.id, update.message.from_user.full_name)

    send_msg(bot, update, user.msg_ativo())

def status(bot, update):
    user = get_user(engine, update.message.chat_id)

    if user is None:
        insert_new_user_to_db(engine, update.message.from_user.id, update.message.from_user.full_name)

    send_msg(bot, update, user.msg_ativo())

def insert_new_user_to_db(engine, telegram_id, name, active=True):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    entry = TelegramUser(id=telegram_id, name=name, active=active)
    session.add(entry)
    session.commit()
    return

def get_user(engine, telegram_id):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    result = session.query(TelegramUser).filter(TelegramUser.id == telegram_id).first()
    return result

def has_user(engine, telegram_id):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    result = session.query(TelegramUser).filter(TelegramUser.id == telegram_id).count()
    return result == 1

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
        CommandHandler('wod', wod)
    )
    dispatcher.add_handler(
        CommandHandler('liga', liga)
    )
    dispatcher.add_handler(
        CommandHandler('desliga', desliga)
    )
    dispatcher.add_handler(
        CommandHandler('status', status)
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
    from common import get_config, CONFIG_PATH, get_uri

    settings = get_config()

    if not CONFIG_PATH:
        print("Error, no config file")
        sys.exit(1)

    if ("main" not in settings) or ("token" not in settings["main"]):
        print("Error, no token in config file")

    TELEGRAM_TOKEN = settings["main"]["token"]

    print("press CTRL + C to cancel.")    

    init_db(get_uri(settings))

    engine = create_engine(get_uri(settings))
    main()
