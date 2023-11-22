import telebot
from pytube import YouTube
import glob
import os
import time

token = 'my_token'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Привет, отправляешь ссылку на youtube ролик, и бот присылает тебе файл с музыкой')


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Привет, бот пока ничего не умеет, кроме создания аудио файлов на основе ссылки Youtube.\nВ формате: https://youtu.be/... или https://www.youtube.com/...')


@bot.message_handler(commands=['github'])
def github_project_url(message):
    bot.send_message(message.chat.id, 'Ссылка на github проекта: ')


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if 'https://www.youtube.com' in message.text or 'https://youtu.be' in message.text:
        send_audio(message)
    else:
        bot.send_message(message.chat.id, 'Напиши /help, чтобы узнать что умеет бот')


def create_audio(link):
    yt = YouTube(link.strip())
    audio = yt.streams.filter(only_audio=True).first().download('FOR_MUSIC')  # Скачиваю файл с музыкой в формате mp4 в каталог FOR_MUSIC
    return audio


def send_audio(message):
    try:
        music = open(create_audio(message.text), 'rb')
        bot.send_audio(message.chat.id, music)
        music.close()
    except Exception as exc:
        bot.send_message(message.chat.id, 'Некорректная ссылка')
        print(exc, '\nerror: send_audio')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            files = glob.glob('Директория для удаления файлов после перезапуска бота*.mp4')
            for f in files:
                os.remove(f)
            time.sleep(3)
            print(ex, '\nerror: polling')
