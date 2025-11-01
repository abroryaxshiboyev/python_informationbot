import telebot
from telebot import types
import json
from flask import Flask, request
import os

TOKEN = "6099999527:AAHuAytaxvv1DdZ82pmnOp4KtQ4kn7xSLTs" 
bot = telebot.TeleBot(TOKEN)
admin_chat_id=1566208883
# admin_chat_id = 878025138  # o‘rningga o‘zingning chat_id ni yoz

# Flask ilova
app = Flask(__name__)

menu1 = '📚Kitoblar'
menu2 = "Video qo'llanma"
menu3 = "📃Nazariy ma'lumotlar"
menu4 = "📝Topshiriqlar"
menu5 = "🌐Manbalar"
menu6 = "📞Aloqa"

bosh_sahifa = "Bosh sahifa"
orqaga = "⬅orqaga"
qoshish = "qo'shish"


@bot.message_handler(commands=['start'])
def start(message):
    with open("menu.json", "r") as file:
        menu = json.load(file)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(menu1)
    item2 = types.KeyboardButton(menu2)
    item3 = types.KeyboardButton(menu3)
    item4 = types.KeyboardButton(menu4)
    item5 = types.KeyboardButton(menu5)
    item6 = types.KeyboardButton(menu6)
    markup.add(item1, item2, item3, item4, item5, item6)
    for key in [menu1, menu2, menu3, menu4, menu5, menu6, bosh_sahifa]:
        if message.chat.id in menu[key]:
            menu[key].remove(message.chat.id)
    menu[bosh_sahifa].append(message.chat.id)
    with open("menu.json", "w") as file:
        json.dump(menu, file)
    bot.send_message(message.chat.id, f"Salom, {message.from_user.first_name}", reply_markup=markup)


@bot.message_handler(content_types=['text', 'video', 'video_note', 'document'])
def bot_message(message):
    with open("add.json", "r") as file:
        add = json.load(file)
    with open("data.json", "r") as file:
        data = json.load(file)
    with open("menu.json", "r") as file:
        menu = json.load(file)

    if message.chat.type == 'private':
        if message.text == qoshish and message.chat.id == admin_chat_id:
            with open("add.json", "w") as file:
                json.dump({"add": True, "name": message.text, "commit": False}, file)
            bot.send_message(message.chat.id, "Qo'shmoqchi bo'lgan menyu nomini kiriting")
        elif add['add'] and message.chat.id == admin_chat_id:
            with open("add.json", "w") as file:
                json.dump({"add": False, "name": message.text, "commit": True}, file)
            bot.send_message(message.chat.id, "Qo'shmoqchi bo'lgan xabaringizni kiriting")
        elif add["commit"] and message.chat.id == admin_chat_id:
            menuButton = None
            for key in [menu1, menu2, menu3, menu4, menu5, menu6]:
                if message.chat.id in menu[key]:
                    menuButton = key
                    break
            if menuButton:
                data[menuButton].append({"text": add["name"], "id": message.id, "chat": message.chat.id, "menu": []})
                with open("data.json", "w") as file:
                    json.dump(data, file)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in data[menuButton]:
                    markup.add(types.KeyboardButton(i['text']))
                if message.chat.id == admin_chat_id:
                    markup.add(types.KeyboardButton(qoshish))
                markup.add(types.KeyboardButton(orqaga))
                bot.send_message(message.chat.id, f"Bu {menuButton} ga qo'shildi", reply_markup=markup)
                with open("add.json", "w") as file:
                    json.dump({"add": False, "name": message.text, "commit": False}, file)
        elif message.text == orqaga:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in [menu1, menu2, menu3, menu4, menu5, menu6]:
                markup.add(types.KeyboardButton(i))
            for key in [menu1, menu2, menu3, menu4, menu5, menu6, bosh_sahifa]:
                if message.chat.id in menu[key]:
                    menu[key].remove(message.chat.id)
            menu[bosh_sahifa].append(message.chat.id)
            with open("menu.json", "w") as file:
                json.dump(menu, file)
            bot.send_message(message.chat.id, "Bosh menyudasiz", reply_markup=markup)
        else:
            for key in [menu1, menu2, menu3, menu4, menu5, menu6]:
                if message.chat.id in menu[key]:
                    for i in data[key]:
                        if message.text == i['text']:
                            bot.copy_message(message.chat.id, i['chat'], i['id'])
                    return
            if message.chat.id in menu[bosh_sahifa]:
                if message.text in [menu1, menu2, menu3, menu4, menu5, menu6]:
                    menuButton = message.text
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for i in data[menuButton]:
                        markup.add(types.KeyboardButton(i['text']))
                    if message.chat.id == admin_chat_id:
                        markup.add(types.KeyboardButton(qoshish))
                    markup.add(types.KeyboardButton(orqaga))
                    for key in [menu1, menu2, menu3, menu4, menu5, menu6, bosh_sahifa]:
                        if message.chat.id in menu[key]:
                            menu[key].remove(message.chat.id)
                    menu[menuButton].append(message.chat.id)
                    with open("menu.json", "w") as file:
                        json.dump(menu, file)
                    bot.send_message(message.chat.id, f"{menuButton}dan birini tanlang:", reply_markup=markup)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME")}/{TOKEN}')
    return "Webhook set", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    print("✅ Bot Flask server orqali ishga tushdi (webhook mode)")
    app.run(host='0.0.0.0', port=port)
