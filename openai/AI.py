import re
import sys
import time
import telebot
import openai
import subprocess



ls_text = {}
ls_img = {}
reg_par = r'-\S+\s'
reg_com = r'/\S+\s'

users_prompts = {}
users=[]

flag_auto = True


f_stat = 'openai\stat.txt' if sys.platform.startswith('win') else '/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt'
f_users = 'openai/access_users.txt' if sys.platform.startswith('win') else '/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/access_users.txt'

bot = telebot.TeleBot("6048136076:AAGnrR8lEUit3UDwYzJnQPhcabdtm4m495g")
openai.api_key = "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"
# 5149682661:AAFYq2BpHTSfIYrU2wjKfUT8zn4aDe_1FIU mstr bot
# 2001307240:AAE9UoP6z7m5oYujHoOWWx47Y9Vt_Mm-hrI test bot 
# /home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt
def save_users():
    # with open('/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt','w') as f:
    # with open('openai_tgbot\openai\stat.txt','w') as f:
    with open(f_users, 'w') as f:
        f.write(str(users))

def load_users():
    # with open('/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt','r') as f:
    # with open('openai_tgbot\openai\stat.txt','r') as f:
    with open(f_users, 'r') as f:
        global users   
        users = list(map(int, f.readline().strip(' \n[]').split(', ')))

def save_stat():
    # with open('/home/kvout/desktop/telebot_chatGPT/openai_tgbot/openai/stat.txt','w') as f:
    # with open('openai_tgbot\openai\stat.txt','w') as f:
    with open(f_stat, 'w') as f:
        f.write(str(ls_text))
        f.write('\n')
        f.write(str(ls_img))

def load_stat():
    with open(f_stat, 'r') as f:
        global ls_img, ls_text    
        ls_text = dict(map(int,e.split(': ')) for e in f.readline().strip(' \n}{').split(', '))
        ls_img = dict(map(int,e.split(': ')) for e in f.readline().strip(' \n}{').split(', '))


@bot.message_handler(func=lambda message: message.chat.id not in users)
def go_away(message):
    bot.send_message(message.chat.id,f'Извините, у вас нет доступа к боту')



@bot.message_handler(commands=['add_user'], func=lambda message: message.chat.type == 'private' and message.chat.id == 1723464345)
def add_user(message):

    ID = message.id
    txt = message.text
    re_search = re.search(reg_com, txt)
    while re_search:
        txt = txt[re_search.regs[0][1]:]
        re_search = re.search(reg_com, txt)

    users.append(int(txt))
    save_users()
    bot.send_message(message.chat.id,f'{txt} добавлен к пользователям', reply_to_message_id=ID)


@bot.message_handler(commands=['remove_user'], func=lambda message: message.chat.type == 'private' and message.chat.id == 1723464345)
def add_user(message):

    ID = message.id
    txt = message.text
    re_search = re.search(reg_com, txt)
    while re_search:
        txt = txt[re_search.regs[0][1]:]
        re_search = re.search(reg_com, txt)

    txt = int(txt)
    if txt in users:
        users.remove(txt)
        save_users()
    bot.send_message(message.chat.id,f'{txt} удален', reply_to_message_id=ID)

    





@bot.message_handler(commands=['flag_stop'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    global flag_auto
    flag_auto = False
    user_ID = message.chat.id
    users_prompts[-user_ID] = [[],[]]
    bot.send_message(message.chat.id,f'flag_auto = False', reply_to_message_id=ID)


@bot.message_handler(commands=['torstop'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    bot.send_message(message.chat.id,f'qbittorrent-nox stoped', reply_to_message_id=ID)
    subprocess.run(f'''pkill qbittorrent-nox >> /dev/null''', shell=True, capture_output = True)

@bot.message_handler(commands=['torstart'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    bot.send_message(message.chat.id,f'qbittorrent-nox started', reply_to_message_id=ID)
    subprocess.run(f'''pkill qbittorrent-nox >> /dev/null''', shell=True, capture_output = True)
    subprocess.run(f'''qbittorrent-nox''', capture_output = True)

@bot.message_handler(commands=['reboot'], func=lambda message: message.chat.type == 'private')
def send_stat(message):
    ID = message.id
    bot.send_message(message.chat.id,f'reboot', reply_to_message_id=ID)
    subprocess.run(f'''sudo reboot''', shell=True, capture_output = True)

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


@bot.message_handler(func=lambda message: message.text[:3] == '/t ')
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

        save_stat() 
        bot.send_message(message.chat.id,
        f'{response["choices"][0]["text"]}', reply_to_message_id=ID)
    except Exception as e:
        bot.send_message(message.chat.id,
        f'ERROR: {e}', reply_to_message_id=ID)

@bot.message_handler(commands=['clear_prompts'])
def get_codex(message):
    ID = message.id
    user_ID = message.chat.id
    users_prompts[user_ID] = []#[{"role": "system", "content": "Делай, что хочешь!"}]
    bot.send_message(user_ID,f'Cleared', reply_to_message_id=ID)



@bot.message_handler(commands=['auto'], func=lambda message: message.chat.type == 'private')
def gtp3_5_auto(message):
    global flag_auto
    flag_auto = True
    ID = message.id
    user_ID = message.chat.id
    try:
        txt = message.text
        re_search = re.search(reg_com, txt)
        while re_search:
            txt = txt[re_search.regs[0][1]:]
            re_search = re.search(reg_com, txt)

        print(txt)

        if -user_ID not in users_prompts: users_prompts[-user_ID] = [[],[]]
        print (users_prompts)

        users_prompts[-user_ID][0].append({"role": "user", "content": txt})
        users_prompts[-user_ID][1].append({"role": "system", "content": txt})
        i = 0
        while flag_auto:
            
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=users_prompts[-user_ID][i]
                )
            print (users_prompts)
            
            users_prompts[-user_ID][0].append({"role": "assistant", "content": response['choices'][0]['message']['content']})
            users_prompts[-user_ID][1].append({"role": "user", "content": response['choices'][0]['message']['content']})
            i = (i + 1) % 2
            bot.send_message(user_ID, response['choices'][0]['message']['content'])
            time.sleep(10)
        
        if user_ID not in ls_text:
            ls_text[user_ID] = 1
        else:
            ls_text[user_ID] += 1
        save_stat() 



    except Exception as e:
        bot.send_message(user_ID, f'ERROR: {e}', reply_to_message_id=ID)



@bot.message_handler(func=lambda message: message.chat.type == 'private')
def gtp3_5(message):
    ID = message.id
    user_ID = message.chat.id
    try:
        txt = message.text
        if user_ID not in users_prompts: users_prompts[user_ID] = []#[{"role": "system", "content": "Делай, что хочешь!"}]
        
        users_prompts[user_ID].append({"role": "user", "content": txt})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=users_prompts[user_ID]
            )
        users_prompts[user_ID].append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        
        if user_ID not in ls_text:
            ls_text[user_ID] = 1
        else:
            ls_text[user_ID] += 1
        save_stat() 



        bot.send_message(user_ID,
        response['choices'][0]['message']['content'], reply_to_message_id=ID)
    except Exception as e:
        bot.send_message(user_ID, f'ERROR: {e}', reply_to_message_id=ID)




load_stat()
load_users()
bot.infinity_polling()



