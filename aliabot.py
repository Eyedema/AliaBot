import sys
import asyncio
import random
import requests
import re
import csv
import json
import telepot
from bot_api_key import api_token
import bot_utilities
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space, include_callback_query_chat_id


class Player(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
    
    def _hint(self, msg):
        hint_number = [key for key, value in ROAD_DICTIONARY.items() if msg in key]
        hint = [[key, value] for key, value in ROAD_DICTIONARY.items() if msg in key]
        text = ""
        for a, b in enumerate(hint_number, 1):
            text += '{}: {}\n'.format(a, b) 
        keyboard = [[]]
        counter = 1
        for item in hint:
            keyboard[0].append(InlineKeyboardButton(text=str(counter), callback_data=item[1]))
            counter += 1
        return [keyboard, text]

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            await self.sender.sendMessage('Non mandare messaggi multimediali, grazie.')
            return
        road = msg['text'].upper()
        try:
            code = ROAD_DICTIONARY[road]
            await self.sender.sendMessage(newbot.get_schedule(code))
        except KeyError:
            keyboard = InlineKeyboardMarkup(inline_keyboard=self._hint(road)[0])
            try:
                await self.sender.sendMessage(self._hint(road)[1])
                sent = await self.sender.sendMessage('Quale delle strade vuoi cercare?', reply_markup=keyboard)
                self._editor = telepot.aio.helper.Editor(self.bot, sent)
            except telepot.exception.TelegramError:
                await self.sender.sendMessage("Nessuna corrispondenza trovata.")


    async def on_callback_query(self, msg):
        await self._cancel_last()
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        result = newbot.get_schedule(query_data)
        await self.sender.sendMessage(result)

    async def _cancel_last(self):
        if self._editor:
            await self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None


TOKEN = api_token
ROAD_DICTIONARY = newbot.build_dictionary()
bot = telepot.aio.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
           per_chat_id(), create_open, Player, timeout=10),
])
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Bot active, listening...')

loop.run_forever()