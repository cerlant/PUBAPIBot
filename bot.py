import os, time
import logging
import ccxt.binance as binance
from telegram.ext import Updater, CommandHandler, run_async

TOKEN = os.environ['TOKEN']
PORT = os.environ['PORT']
USE_WEBHOOK =  os.environ['USE_WEBHOOK'] or False

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Helloo')

@run_async
def get_ticker(update, context):
    time.sleep(1)
    print(type(context.args[0]))
    ticker = binance().fetch_ticker(symbol=context.args[0])
    if ticker['info']: del ticker['info']
    text = ''
    for k,v in ticker.items():
        text += k.capitalize() +': '+str(v)+'\n'
    text += 'ChatId:' + str(update.effective_chat.id)
    print(text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('get_ticker', get_ticker))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if USE_WEBHOOK:
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook('https://pubapibot.herokuapp.com/' + TOKEN)
        logger.info('running on webhook...')
    else:
        updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
