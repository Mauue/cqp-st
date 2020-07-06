from aiocqhttp import CQHttp, Event, Message, MessageSegment
import db
import main


bot = CQHttp(api_root='http://127.0.0.1:5699')
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
        url = main.get_random_img_in_file()
        if url is None:
            return {'reply': "没用库存了"}
        img = MessageSegment.image('temp/'+url)
        await bot.send(event, img)
    elif message.startswith("#下载"):
        num = message.replace('#下载', '', 1)
        if not num:
            num = 10
        m = await main.random_download(num)
        return {'reply': '已下载{}张图片'.format(m)}


@bot.on_message('group')
async def _g(event: Event):
    message = str(event.message)
    if message == '#涩图':
        filename = main.get_random_img_in_file()
        if filename is None:
            return {'reply': "没用库存了"}
        img = MessageSegment.image('temp/' + filename)
        await bot.send(event, img)
        main.delete_image(filename)
        db.mark_image(filename.split('.')[0])


bot.run(host='127.0.0.1', port=7890)