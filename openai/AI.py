import re
import telebot
import openai
import subprocess



ls_text = {}
ls_img = {}
reg_par = r'-\S+\s'
reg_com = r'/\S+\s'

bot = telebot.TeleBot("6048136076:AAGnrR8lEUit3UDwYzJnQPhcabdtm4m495g")
openai.api_key = "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"
# 5149682661:AAFYq2BpHTSfIYrU2wjKfUT8zn4aDe_1FIU mstr bot
# 2001307240:AAE9UoP6z7m5oYujHoOWWx47Y9Vt_Mm-hrI test bot 
# /home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt
def save_stat():
    with open('/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt','w') as f:
    # with open('openai_tgbot\openai\stat.txt','w') as f:
        f.write(str(ls_text))
        f.write('\n')
        f.write(str(ls_img))
def load_stat():
    with open('/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt','r') as f:
    # with open('openai_tgbot\openai\stat.txt','r') as f:
        global ls_img, ls_text    
        ls_text = dict(map(int,e.split(': ')) for e in f.readline().strip(' \n}{').split(', '))
        ls_img = dict(map(int,e.split(': ')) for e in f.readline().strip(' \n}{').split(', '))
    

@bot.message_handler(commands=['torstop'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    bot.send_message(message.chat.id,f'qbittorrent-nox stoped', reply_to_message_id=ID)
    subprocess.run(f'''pkill qbittorrent-nox >> /dev/null''', shell=True, capture_output = True)

@bot.message_handler(commands=['torstart'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    bot.send_message(message.chat.id,f'qbittorrent-nox started', reply_to_message_id=ID)
    subprocess.run(f'''qbittorrent-nox''', capture_output = True)

@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.text[:7] == 'magnet:')
def torrent(message):
    txt = message.text
    ID = message.id
    # subprocess.run(f'''qbittorrent-nox''', capture_output = True)
    subprocess.run(f'''qbittorrent-nox {txt}''', shell=True)
    bot.send_message(message.chat.id,f'Torrent started', reply_to_message_id=ID)

@bot.message_handler(commands=['stat'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    bot.send_message(message.chat.id,f'Text requests:\n{ls_text}', reply_to_message_id=ID)
    bot.send_message(message.chat.id,f'Img requests:\n{ls_img}', reply_to_message_id=ID)

@bot.message_handler(commands=['img'])
def get_codex(message):
    N = 4
    Q = '1024x1024'
    txt = message.text
    re_search = re.search(reg_com, txt)
    while re_search:
        txt = txt[re_search.regs[0][1]:]
        re_search = re.search(reg_com, txt)

    re_search = re.search(reg_par, txt)
    while re_search:

        par = txt[re_search.regs[0][0] + 1:re_search.regs[0][1] - 1]
        if par.isdigit():
            try:
                N = int(par)
            except Exception as e:
                bot.send_message(message.chat.id,
                f'BAD_NUMBER: {e}', reply_to_message_id=ID)
        elif par.lower() == 'hi':
            Q = '1024x1024'
        elif par.lower() == 'lo':
            Q = '256x256'
        

        txt = txt[re_search.regs[0][1]:]
        re_search = re.search(reg_par, txt)



    ID = message.id
    try:
        
        response = openai.Image.create(
        prompt=txt,
        n=N,
        size=Q,
        )
        
        cont = []
        for i in response["data"]:
            cont.append(telebot.types.InputMediaPhoto(i["url"]))
        
        bot.send_media_group(message.chat.id, cont, reply_to_message_id=ID)


        if message.chat.id not in ls_img:
            ls_img[message.chat.id] = 1
        else:
            ls_img[message.chat.id] += 1

        save_stat()
        # print ('IMG')
        # print (ls_img)
    except Exception as e:
        bot.send_message(message.chat.id,
        f'ERROR: {e}', reply_to_message_id=ID)


@bot.message_handler(func=lambda message: message.chat.type == 'private' or message.text[:3] == '/t ')
def get_codex(message):
    ID = message.id
    try:
        txt = message.text
        re_search = re.search(reg_com, txt)
        while re_search:
            txt = txt[re_search.regs[0][1]:]
            re_search = re.search(reg_com, txt)

        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=txt,
            temperature=0,
            max_tokens=3500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['"""'])
        
        if message.chat.id not in ls_text:
            ls_text[message.chat.id] = 1
        else:
            ls_text[message.chat.id] += 1

        # print ('TEXT')
        # print (ls_text)
        save_stat() 
        bot.send_message(message.chat.id,
        f'{response["choices"][0]["text"]}', reply_to_message_id=ID)
    except Exception as e:
        bot.send_message(message.chat.id,
        f'ERROR: {e}', reply_to_message_id=ID)




load_stat()
bot.infinity_polling()



