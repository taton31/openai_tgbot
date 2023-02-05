import telebot
import sys


bot = telebot.TeleBot("6048136076:AAGnrR8lEUit3UDwYzJnQPhcabdtm4m495g")
# 5149682661:AAFYq2BpHTSfIYrU2wjKfUT8zn4aDe_1FIU mstr bot
# 2001307240:AAE9UoP6z7m5oYujHoOWWx47Y9Vt_Mm-hrI test bot 
# /home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt
bot.send_message('1723464345','asdf')


if __name__ == "__main__":
    for param in sys.argv:
        print (param)
