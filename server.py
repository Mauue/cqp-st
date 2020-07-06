from aiocqhttp import CQHttp, Event, Message, MessageSegment
import db
import main


bot = CQHttp()
s = main.SearchMachine()

@bot.on_message('private')
async def _(event: Event):
    message = str(event.message)
    if message == '#初始化':
        db.init()
        return {'reply': "初始化完成"}
    elif message == '#库存':
        count = db.count_img()
        return {'reply': "剩余:{}".format(count)}
    elif message.startswith('#搜索'):
        tag = message.replace('#搜索', '', 1)
        if not tag:
            return {'reply': "需要搜索tag"}
        m = s.search(tag)
        return {'reply': m}
    elif message == '#涩图':
        url = db.get_img_url(mark=False)
        return {'reply': url}


@bot.on_message('group')
async def _g(event: Event):
   pass


bot.run(host='127.0.0.1', port=7890)