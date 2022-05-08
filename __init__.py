from asyncio.windows_events import NULL
from distutils.sysconfig import get_python_lib
import json
import os
import httpx
from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher import Matcher
from .utils import SplatoonInfo
from .config import Config
from nonebot.plugin import require
from nonebot import get_bots
from nonebot.permission import  SUPERUSER
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

global_config = get_driver().config
config = Config.parse_obj(global_config)

__splatoon2_tools_version__ = "v1.0.4"
# group_id_list=[901729597]
group_id_list=[901729597,100094234,961179787]

matcher_weapon_power = on_command('主强')
matcher_skill_forward = on_command('品牌倾向')
matcher_weapon_distance = on_command('武器射程')
matcher_weapon_infomation = on_command('武器详情')
matcher_kill = on_command('伪确')
matcher_pool = on_command('开泉')

salmon_run = on_command('打工', aliases={'工'})
regular_battle = on_command('涂地', aliases={'涂地','塗地'})
ranked_battle = on_command('单排', aliases={'单排','單排'})
league_battle = on_command('组排', aliases={'组排','組排'})
update = on_command('更新地图数据')
admin_send= on_command('发送地图推送', permission=SUPERUSER)

scheduler = require("nonebot_plugin_apscheduler").scheduler
splatoonclass=None

@matcher_weapon_distance.handle()
async def _(matcher: Matcher):
    await matcher_weapon_distance.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapons Distance', format_name='jpg')),
            cache=False,
        )
    )


@matcher_weapon_infomation.handle()
async def _(matcher: Matcher):
    await matcher_weapon_infomation.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapons Information', format_name='jpg')),
            cache=False,
        )
    )


@matcher_weapon_power.handle()
async def _(matcher: Matcher):
    await matcher_weapon_power.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapon Plus Power', format_name='jpg')),
            cache=False,
        )
    )


@matcher_skill_forward.handle()
async def _(matcher: Matcher):
    await matcher_skill_forward.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Skill Forward', format_name='jpg')),
            cache=False,
        )
    )

@matcher_pool.handle()
async def _(matcher: Matcher):
    res = get_file(get_info(get_coop_schedule()['details'][0])['stage'] + ' Pool', format_name='jpg')
    await matcher_pool.send(
        MessageSegment.image(
            file=image_to_base64(res),
            cache=False
        )
    )

@regular_battle.handle()
async def _handle(matcher: Matcher):
    get_splatoonclass()
    await salmon_run.finish(MessageSegment.image(splatoonclass.get_regular_battle()))


@ranked_battle.handle()
async def _handle(matcher: Matcher):
    get_splatoonclass()
    await salmon_run.finish(MessageSegment.image(splatoonclass.get_ranked_battle()))


@league_battle.handle()
async def _handle(matcher: Matcher):
    get_splatoonclass()
    await salmon_run.finish(MessageSegment.image(splatoonclass.get_League_Battle()))


@salmon_run.handle()
async def _handle(matcher: Matcher):
    get_splatoonclass()
    await salmon_run.finish(MessageSegment.image(splatoonclass.get_salmon_run()))

@update.handle()
async def _handle(matcher: Matcher):
    global splatoonclass
    splatoonclass=None
    await update.finish("地图已更新")

@admin_send.handle()
async def _handle(matcher: Matcher):
    get_splatoonclass()
    bot=get_bots()["2807672204"]
    forward_msg=[]
    forward_msg.append(to_json("这里是Splatoon2定时推送姬,以下是未来时间段的地图信息！"))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_regular_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_ranked_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_League_Battle()))))
    try:
        forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_salmon_run()))))
        forward_msg.append(to_json("这个是当前打工的开泉图，请签收！"))
        forward_msg.append(to_json(Message(MessageSegment.image(image_to_base64(get_file(get_info(get_coop_schedule()['details'][0])['stage'] + ' Pool', format_name='jpg'))))))
        forward_msg.append(to_json("Master QQ：1557157806"))
    except:
        forward_msg.append(to_json('打工地图获取失效，这可能是由于打工未开放导致的'))
        print("打工地图获取失效，这可能是由于打工未开放导致的")
    for group_id in group_id_list:
        try:
            await bot.send_group_forward_msg(group_id=group_id,messages=forward_msg)
        except:
            print("推送群消息出现错误")
#定时清空Splatoonclass
@scheduler.scheduled_job(
    'cron',
    hour="*/2",
    minute=1,
)
async def _():
    global splatoonclass
    splatoonclass=None


#定时推送图片
@scheduler.scheduled_job(
    'cron',
    hour="*/2",
    minute=3,
)
async def _():
    get_splatoonclass()
    bot=get_bots()["2807672204"]
    forward_msg=[]
    forward_msg.append(to_json("这里是Splatoon2定时推送姬,以下是未来时间段的地图信息！"))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_regular_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_ranked_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_League_Battle()))))
    try:
        forward_msg.append(to_json(Message(MessageSegment.image(splatoonclass.get_salmon_run()))))
        forward_msg.append(to_json("这个是当前打工的开泉图，请签收！"))
        forward_msg.append(to_json(Message(MessageSegment.image(image_to_base64(get_file(get_info(get_coop_schedule()['details'][0])['stage'] + ' Pool', format_name='jpg'))))))
        forward_msg.append(to_json("Master QQ：1557157806"))
    except:
        forward_msg.append(to_json('打工地图获取失效，这可能是由于打工未开放导致的'))
        print("打工地图获取失效，这可能是由于打工未开放导致的")
    for group_id in group_id_list:
        try:
            await bot.send_group_forward_msg(group_id=group_id,messages=forward_msg)
        except:
            print("推送群消息出现错误")

def get_splatoonclass():
    global splatoonclass
    if(splatoonclass!=None):
        if(splatoonclass.html==""):
            splatoonclass=None
    while(splatoonclass==None):
        if(splatoonclass==None):
            try:
                splatoonclass=SplatoonInfo()
            except:
                print("访问地图网页出错，正在尝试重新访问")
    return

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()


def get_file(name, format_name='png'):
    path=os.path.join(os.path.dirname(__file__), "resource")
    img = Image.open(os.path.join(path, '{}.{}'.format(name, format_name)))
    return img
    
def get_coop_schedule():
    with httpx.Client() as client:
        result = client.get('https://splatoon2.ink/data/coop-schedules.json')
        return json.load(result)

def get_info(res):
    return {
        'stage': res['stage']['name'],
        'start_time': res['start_time'],
        'end_time': res['end_time'],
        'weapons': [get_weapon_name(w) for w in res['weapons']]
    }

def get_weapon_name(res):
    if 'weapon' not in res:
        return res['coop_special_weapon']['name']
    else:
        return res['weapon']['name']

def to_json(msg: Message):
        return {"type": "node", "data": {"name": "Splatoon2定时地图推送姬", "uin": 2807672204, "content": msg}}