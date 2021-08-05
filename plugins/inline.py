# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)


import requests
from requests.utils import requote_uri
from pyrogram import Client, filters 
from pyrogram.types import *
from .commands import *
from .info import *


@Client.on_inline_query()
async def inline_info(bot, update):
    query = update.query
    if "+" in query:
        movie_name, number = query.split("+", -1)
    else:
        movie_name = query
    r = requests.get(API + requote_uri(movie_name))
    if number:
        movies = [r.json()[int(number) - 1]]
    else:
        movies = r.json()
    answers = []
    for movie in movies:
        description = movie['title'] if movie['title'] else None
        description += f" - {movie['type'].capitalize()}" if movie['type'] else None
        description += f" - ({str(movie['release_year'])})" if movie['release_year'] else None
        photo = thumb(movie)
        movie_info = info(movie)
        keyboard = BUTTONS
        answers.append(
            InlineQueryResultArticle(
                title=movie['title'],
                thumb_url=photo,
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text=movie_info,
                    disable_web_page_preview=True
                ),
                reply_markup=keyboard
            )
        )
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )
