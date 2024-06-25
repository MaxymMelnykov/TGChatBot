from callbacks import setup_callbacks
from config import bot

if __name__ == '__main__':
    setup_callbacks(bot)
    bot.polling(none_stop=True)
