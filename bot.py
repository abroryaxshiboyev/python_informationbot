import telebot
from telebot import types
import json


TOKEN='6099999527:AAHuAytaxvv1DdZ82pmnOp4KtQ4kn7xSLTs'
bot=telebot.TeleBot(TOKEN)

admin_chat_id=878025138
# admin_chat_id=1566208883
menu1='📚Kitoblar'
menu2="Video qo'llanma"
menu3="📃Nazariy ma'lumotlar"
menu4="📝Topshiriqlar"
menu5="🌐Manbalar"
menu6="📞Aloqa"

bosh_sahifa="Bosh sahifa"
orqaga="⬅orqaga"
qoshish="qo'shish"


@bot.message_handler(commands=['start'])
def start(message):
    with open("menu.json", "r") as file:
        menu = json.load(file)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(menu1)
    item2 = types.KeyboardButton(menu2)
    item3 = types.KeyboardButton(menu3)
    item4=types.KeyboardButton(menu4)
    item5 = types.KeyboardButton(menu5)
    item6 = types.KeyboardButton(menu6)
    markup.add(item1,item2,item3,item4,item5,item6)
    if (message.chat.id in menu[menu1]):
        menu[menu1].remove(message.chat.id)
    if (message.chat.id in menu[menu2]):
        menu[menu2].remove(message.chat.id)
    if (message.chat.id in menu[menu3]):
        menu[menu3].remove(message.chat.id)
    if (message.chat.id in menu[menu4]):
        menu[menu4].remove(message.chat.id)
    if (message.chat.id in menu[menu5]):
        menu[menu5].remove(message.chat.id)
    if (message.chat.id in menu[menu6]):
        menu[menu6].remove(message.chat.id)
    if (message.chat.id in menu[bosh_sahifa]):
        menu[bosh_sahifa].remove(message.chat.id)
    menu[bosh_sahifa].append(message.chat.id)
    with open("menu.json", "w") as file:
        json.dump(menu, file)
    bot.send_message(message.chat.id,'Salom,{0.first_name}'.format(message.from_user),reply_markup=markup)
@bot.message_handler(content_types=['text','video','video_note','document'])
def bot_message(message):
    with open("add.json", "r") as file:
        add = json.load(file)
    with open("data.json", "r") as file:
        data = json.load(file)
    with open("menu.json", "r") as file:
        menu = json.load(file)
    if message.chat.type=='private':
        if message.text==qoshish and message.chat.id==admin_chat_id:
            with open("add.json","w") as file:
                json.dump({"add":True,"name":message.text,"commit":False},file)
            bot.send_message(message.chat.id, "qo'shmoqchi bo'lgan menyu nomini kiriting")
        elif add['add'] and message.chat.id==admin_chat_id:
            with open("add.json","w") as file:
                json.dump({"add":False,"name":message.text,"commit":True},file)
            bot.send_message(message.chat.id, "qo'shmoqchi bo'lgan xabaringizni kiriting")
        elif add["commit"] and message.chat.id==admin_chat_id:
            if(message.chat.id in menu[menu1] or message.chat.id in menu[menu2] or message.chat.id in menu[menu3]
            or message.chat.id in menu[menu4] or message.chat.id in menu[menu5] or message.chat.id in menu[menu6]):
                if(message.chat.id in menu[menu1]):
                    menuButton=menu1
                if (message.chat.id in menu[menu2]):
                    menuButton=menu2
                if (message.chat.id in menu[menu3]):
                    menuButton = menu3
                if (message.chat.id in menu[menu4]):
                    menuButton = menu4
                if (message.chat.id in menu[menu5]):
                    menuButton = menu5
                if (message.chat.id in menu[menu6]):
                    menuButton = menu6
                data[menuButton].append({"text": add["name"], "id": message.id, "chat": message.chat.id,"menu":[]})
                with open("data.json", "w") as file:
                    json.dump(data, file)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in data[menuButton]:
                    markup.add(types.KeyboardButton(i['text']))
                if (message.chat.id == admin_chat_id):
                    add = types.KeyboardButton(qoshish)
                    markup.add(add)
                back = types.KeyboardButton(orqaga)
                markup.add(back)
                bot.send_message(message.chat.id, f"bu {menu3} ga qo'shildi",reply_markup=markup)
                with open("add.json","w") as file:
                    json.dump({"add":False,"name":message.text,"commit":False},file)
        elif message.text==orqaga:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(menu1)
            item2 = types.KeyboardButton(menu2)
            item3 = types.KeyboardButton(menu3)
            item4 = types.KeyboardButton(menu4)
            item5 = types.KeyboardButton(menu5)
            item6 = types.KeyboardButton(menu6)
            markup.add(item1,item2,item3,item4,item5,item6)
            if(message.chat.id in menu[menu1] or message.chat.id in menu[menu2] or message.chat.id in menu[menu3]
            or message.chat.id in menu[menu4] or message.chat.id in menu[menu5] or message.chat.id in menu[menu6]):
                if (message.chat.id in menu[menu1]):
                    menu[menu1].remove(message.chat.id)
                if (message.chat.id in menu[menu2]):
                    menu[menu2].remove(message.chat.id)
                if (message.chat.id in menu[menu3]):
                    menu[menu3].remove(message.chat.id)
                if (message.chat.id in menu[menu4]):
                    menu[menu4].remove(message.chat.id)
                if (message.chat.id in menu[menu5]):
                    menu[menu5].remove(message.chat.id)
                if (message.chat.id in menu[menu6]):
                    menu[menu6].remove(message.chat.id)
                if (message.chat.id in menu[bosh_sahifa]):
                    menu[bosh_sahifa].remove(message.chat.id)
                menu[bosh_sahifa].append(message.chat.id)
                with open("menu.json", "w") as file:
                    json.dump(menu, file)
            bot.send_message(message.chat.id, "Bosh menyudasiz", reply_markup=markup)
        elif message.chat.id in menu[menu1]:
            for i in data[menu1]:
                if(message.text==i['text']):
                    bot.copy_message(message.chat.id,i['chat'],i['id'])
        elif message.chat.id in menu[menu2]:
            for i in data[menu2]:
                if(message.text==i['text']):
                    bot.copy_message(message.chat.id,i['chat'],i['id'])
        elif message.chat.id in menu[menu3]:
            for i in data[menu3]:
                if(message.text==i['text']):
                    bot.copy_message(message.chat.id,i['chat'],i['id'])
        elif message.chat.id in menu[menu4]:
            for i in data[menu4]:
                if(message.text==i['text']):
                    bot.copy_message(message.chat.id,i['chat'],i['id'])
        elif message.chat.id in menu[menu5]:
            for i in data[menu5]:
                if(message.text==i['text']):
                    bot.copy_message(message.chat.id,i['chat'],i['id'])
        elif message.chat.id in menu[menu6]:
            for i in data[menu6]:
                if(message.text==i['text']):
                    bot.copy_message(message.chat.id,i['chat'],i['id'])
        elif message.chat.id in menu[bosh_sahifa]:
            if(message.text==menu1 or message.text==menu2 or message.text==menu3
                    or message.text==menu4 or message.text==menu5 or message.text==menu6):
                if(message.text==menu1):
                    menuButton=menu1
                if (message.text == menu2):
                    menuButton = menu2
                if (message.text == menu3):
                    menuButton = menu3
                if (message.text == menu4):
                    menuButton = menu4
                if (message.text == menu5):
                    menuButton = menu5
                if (message.text == menu6):
                    menuButton = menu6
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                with open("data.json", "r") as file:
                    data = json.load(file)

                for i in data[menuButton]:
                    markup.add(types.KeyboardButton(i['text']))
                if (message.chat.id == admin_chat_id):
                    add = types.KeyboardButton(qoshish)
                    markup.add(add)
                back = types.KeyboardButton(orqaga)
                markup.add(back)
                if (message.chat.id in menu[menu1]):
                    menu[menu1].remove(message.chat.id)
                if (message.chat.id in menu[menu2]):
                    menu[menu2].remove(message.chat.id)
                if (message.chat.id in menu[menu3]):
                    menu[menu3].remove(message.chat.id)
                if (message.chat.id in menu[menu4]):
                    menu[menu4].remove(message.chat.id)
                if (message.chat.id in menu[menu5]):
                    menu[menu5].remove(message.chat.id)
                if (message.chat.id in menu[menu6]):
                    menu[menu6].remove(message.chat.id)
                if (message.chat.id in menu[bosh_sahifa]):
                    menu[bosh_sahifa].remove(message.chat.id)
                menu[menuButton].append(message.chat.id)
                with open("menu.json", "w") as file:
                    json.dump(menu, file)
                bot.send_message(message.chat.id, f"{menuButton}dan birini tanlang:", reply_markup=markup)


print("✅ Bot muvaffaqiyatli ishga tushdi. Foydalanuvchi xabarini kutmoqda...")

bot.polling(none_stop=True)