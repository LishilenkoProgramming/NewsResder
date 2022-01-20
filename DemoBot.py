# (c) TICSIA
#
# demo bot class implementation

import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from  . import config

class DemoBot:
   
    def __init__(self):
        self.__bot = Bot(config.bot_id)
        self.__handlers = {}
        self.__disp = Dispatcher(bot=self.__bot)
        
    async def __main(self):      
        try:            
            await self.__disp.start_polling()
        finally:
            await self.__bot.close()
                    
   
    def run(self):
        print('Bot run in polling mode. Please CTRL-Break for exit...')        
        asyncio.run(self.__main())  
        
    def register_start_handler(self,handler=None):
        async def internal_handler(event):
            if not handler is None:
                result = handler(event.text,self.__bot)
                await event.answer(result[0],parse_mode = types.ParseMode.HTML, reply_markup = result[1])
            else:
                await event.answer(f"Hello {event.from_user.get_mention(as_html=True)} :-)",parse_mode = types.ParseMode.HTML)
             
        self.__disp.register_message_handler(internal_handler,commands = {"start","restart"})
      
        
    def register_text_handler(self,handler,**aux):
        async def internal__handler(event,regexp):
                result = handler(event.text)            
                await event.answer(result,parse_mode = types.ParseMode.HTML)                    
        self.__disp.register_message_handler(internal__handler,**aux)