from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
import begin.index as index
import datetime as dt

TOKEN="5954721314:AAFFh1hIR8e5xRRkgHX8Hd417k4RqkPPJEM"
now = dt.datetime.now()

def route(update, context):
    if index.define_msg()==True:
        update.message.reply_text("Temperature Records are sent to the chat at "+str(now)+" \n")
    else:
        update.message.reply_text("Device is Offline. Couldn't fetch data.")
    index.final_run()

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', route))
updater.start_polling()

print("Your telegram bot is running!")

updater.idle()