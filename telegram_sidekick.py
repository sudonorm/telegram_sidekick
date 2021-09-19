import os
import warnings
import telegram
import datetime
from telegram.constants import MAX_MESSAGE_LENGTH
from typing import List

class TelegramSidekick:

    def __init__(self):
        pass
    
    def _send_message(self, bot: telegram.Bot, message:str, chat_id:int):
        return bot.send_message(chat_id=chat_id, text=message, parse_mode=None, disable_notification=False, disable_web_page_preview=False)

    def send_message(self, *, messages:List = None, token:str = None, chat_id:int = None, timeout:int = 30):
        """Send message to Telegram bot. """
        
        request = telegram.utils.request.Request(read_timeout=timeout)
        bot = telegram.Bot(token, request=request)
        
        for msg in messages:
            if len(msg) == 0:
                continue
            elif len(msg) > MAX_MESSAGE_LENGTH:
                warnings.warn("This message is longer than the MAX_MESSAGE_LENGTH=%d. Let us split this into smaller messages, shall we?" % MAX_MESSAGE_LENGTH)
                ms = self.chunk_message(msg, MAX_MESSAGE_LENGTH)
                print("That's much better!")
                for msg in ms:
                    self._send_message(bot, msg, chat_id)
            else:
                self._send_message(bot, msg, chat_id)

    def chunk_message(self, msg: List, max_length: int) -> List:
        """Chunk up a long message into smaller messages which are less than the maximum length."""
        
        ms = []
        while len(msg) > max_length:
            ms.append(msg[:max_length])
            msg = msg[max_length:]
        ms.append(msg)
        return ms

    def get_latest_message(self, *, token:str = None, timeout:int = 30):
        """Get the last message sent to a Telegram bot as well as its timestamp"""
        
        request = telegram.utils.request.Request(read_timeout=timeout)
        bot = telegram.Bot(token, request=request)
        
        updates = bot.get_updates(timeout=30)
        
        if not len(updates) == 0:

            dateSent = updates[0]["message"]["date"].strftime('%Y-%m-%d')
            message = updates[0]["message"]["text"]
            
            return message, dateSent, updates
        else:
            raise Exception("No new messages were fetched. The last message needs to have been sent to your bot less than 24 hours ago in order to be able to fetch it. Please send a message to the bot and try again.")

    def get_chat_id(self, *, token:str = None, timeout:int = 30):
        """Get the chat id of a Telegram bot"""
        
        message, dateSent, updates = self.get_latest_message(token=token, timeout=timeout)
    
        return updates[0].message.from_user.id