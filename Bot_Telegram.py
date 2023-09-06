from asyncio import run
from os import getenv
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram import (ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)

load_dotenv()
#colocar as ids do telegram em arquivo env
app = Client(
    'Nome do BOT',
    api_id=getenv('Telegram_API_ID'),
    api_hash=getenv('Telegram_API_Hash'),
    bot_token=getenv('Telegram_Bot_Token')
)
#páginas e botões de callback
@app.on_callback_query()
async def callback(client, callback_query):
    pages = {
        'data': {
            'proximo': InlineKeyboardButton('Proximo', callback_data='page_2'),
            'anterior': InlineKeyboardButton('Anterior', callback_data='data'),
            'texto': 'Você está na página 1'
        },
        'page_2': {
            'proximo': InlineKeyboardButton('Proximo', callback_data='page_2'),
            'anterior': InlineKeyboardButton('Anterior', callback_data='data'),
            'texto': 'Você está na página 2'
        }
    }
    page = pages[callback_query.data]
    await callback_query.edit_message_text(
        page['texto'],
        reply_markup=InlineKeyboardMarkup([[
            page['anterior'], page['Proximo']
        ]])
    )

#colocar botões de escolha
@app.on_message(filters.command('inline'))
async def callback(client, message):
    botoes = InlineKeyboardMarkup(
        [
            [
            InlineKeyboardButton('Callback', callback_data='0'),
            InlineKeyboardButton('link', url='https://docs.pyrogram.org/api/methods/')
            ]
        ]
    )
    await message.reply(
        'Tecla qualquer coisa ai',
        reply_markup=botoes
    )

#para enviar fotos
@app.on_message(filters.command('photo'))
async def foto(client, message):
    app.send_sticker(
        message.chat.id,
        'https://img.freepik.com/psd-gratuitas/menina-poupar-dinheiro-para-o-futuro_1154-299.jpg?w=740&t=st=1694023056~exp=1694023656~hmac=f529e4f3ff152042377db4d0069e708b75705fbcc01ab05e3c1191c7e07ec7e5'
    )
#para enviar sticker
@app.on_message(filters.sticker)
async def figurinha(client, message):
    app.send_sticker(
        message.chat.id,
        message.sticker.file_id
    )
    
#para abrir o teclado na tela
@app.on_message(filters.command('teclado'))
async def teclado(client, message):
    teclado = ReplyKeyboardMarkup(
        [
            ['a', 'b', 'c'],['/ajuda', '/voltar']
        ],
        resize_keyboard=True
    )
    await message.reply(
        'Tecla ai o que você quer',
        reply_markup=teclado
        )
#ao enviar foto ou vídeo resposta com mensagem
@app.on_message(filters.photo | filters.video)
async def photo(client, message):
    print(message.chat.username, message.text)
    await message.reply(message.text + 'Espero que sejam **nudes**, vou vender todos no grupo.')
#ao enviar áudio
@app.on_message(filters.voice | filters.audio)
async def voice(client, message):
    print(message.chat.username, message.text)
    await message.reply(message.text + 'Você não vai pro céu, será que não percebeu que eu sou surdo?')
#comando de ajuda
@app.on_message(filters.command('help'))
async def ajuda(client, message):
    print(message.chat.username, message.text)
    await message.reply(message.text + 'Mensagem de ajuda')
#responder com mensagem
@app.on_message()
async def messages(client, message):
    print(message.chat.username, message.text)
    await message.reply(message.text + '???')
    
app.run()