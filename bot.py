from subprocess import check_output
from subprocess import STDOUT,CalledProcessError
import telebot
from telebot import types #Добавляем импорт кнопок
import time
from telebot.types import InputFile
import os
from datetime import datetime

bot = telebot.TeleBot("")#Токен бота
user_id =  #id вашего аккаунта
download_folder=
@bot.message_handler(content_types=["document"])
def handle_get_file(message):
    try:
        if user_id==message.chat.id:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src=download_folder+"/"+message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,"Файл сохранён")
    except Exception as e:
        bot.reply_to(message, e)
@bot.message_handler(content_types=["photo"])
def get_photo(message):
    try:    
        if user_id==message.chat.id:
            file_info=bot.get_file(message.photo[-1].file_id)
            downloaded_file=bot.download_file(file_info.file_path)
            src=download_folder+"/"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".jpg"
            with open(src,'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,"Файл сохранен под именем - "+src)
    except Exception as e:
        bot.reply_to(message,e)
@bot.message_handler(content_types=["video"])
def get_video(message):
    try:    
        if user_id==message.chat.id:
            file_info=bot.get_file(message.video.file_id)
            downloaded_file=bot.download_file(file_info.file_path)
            src=download_folder+"/"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".mp4"
            with open(src,'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,"Файл сохранен под именем - "+src)
    except Exception as e:
        bot.reply_to(message,e)
@bot.message_handler(content_types=["text"])
def main(message):
       if (user_id == message.chat.id): #проверяем, что пишет именно владелец
                comand = message.text  #текст сообщения
                markup = types.InlineKeyboardMarkup() #создаем клавиатуру
                button = types.InlineKeyboardButton(text="Повторить", callback_data=comand) #создаем кнопку
                markup.add(button) #добавляем кнопку в клавиатуру
                part=comand.split()
                if part[0]=="view":
                	if len(part)==1:
                		bot.send_message(user_id,"В команде view пропущено имя файла")
                	else:
                		f=open(part[1],"rb")
                		bot.send_message(user_id,"Файл отправлен")
                		bot.send_document(user_id,f)
                		#bot.send_message(user_id,str(part[1]))
                else:
                	try: #если команда невыполняемая - check_output выдаст exception
                	    output=check_output(comand,shell=True,stderr=STDOUT)
                	    output=output if output!=bytes("",'utf-8') else "Empty output"
                	    bot.send_message(user_id, output,  reply_markup = markup) #вызываем команду и отправляем сообщение с результатом
                	except CalledProcessError as e:
                	    bot.send_message(user_id, f"Error: {e}\nOutput: {e.output}") #если команда некорректна
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	comand = call.data #считываем команду из поля кнопки data
	try:#если команда не выполняемая - check_output выдаст exception
		markup = types.InlineKeyboardMarkup() #создаем клавиатуру
		button = types.InlineKeyboardButton(text="Повторить", callback_data=comand) #создаем кнопку и в data передаём команду
		markup.add(button) #добавляем кнопку в клавиатуру
		output=check_output(comand,shell=True,stderr=OUTPUT)
		output=output if output!=bytes("",'utf-8') else "Empty output"
		bot.send_message(user_id, output, reply_markup = markup) #вызываем команду и отправляем сообщение с результатом
	except CalledProcessError as e:
		bot.send_message(user_id, "Invalid input - "+e.output) #если команда некорректна

if __name__ == '__main__':
	while True:
		try:#добавляем try для бесперебойной работы
			bot.polling(none_stop=True)#запуск бота
		except:
			time.sleep(10)#в случае падения
