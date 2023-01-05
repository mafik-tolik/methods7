from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN
from bot_commands import *


app = ApplicationBuilder().token(TOKEN).build()


app.add_handler(CommandHandler('hello', hi_command))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('abc', abc_command))
app.add_handler(CommandHandler('candy', candy_command))
app.add_handler(CommandHandler('game', game_command))
app.add_handler(CommandHandler('calculator', calculator_command))
app.add_handler(CommandHandler('phone_book', phone_book_command))


app.run_polling()
