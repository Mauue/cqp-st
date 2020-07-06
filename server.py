from aiocqhttp import CQHttp, Event

bot = CQHttp()


@bot.on_message('private')
async def _(event: Event):
    await bot.send(event, '你发了：')
    return {'reply': event.message}


bot.run(host='127.0.0.1', port=7890)