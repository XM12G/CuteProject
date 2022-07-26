from io import BytesIO
from typing import Union
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message, require
from nonebot.adapters.kaiheila import MessageSegment
from nonebot.params import BotParam
from nonebot.adapters.kaiheila import Bot
require("nonebot_plugin_imageutils")

from .depends import regex
from .data_source import memes
from .utils import Meme, help_image

__plugin_meta__ = PluginMetadata(
    name="表情包制作",
    description="生成各种表情包",
    usage="触发方式：指令 + 文字 (部分表情包需要多段文字)\n发送“表情包制作”查看表情包列表",
    extra={
        "unique_name": "memes",
        "example": "鲁迅说 我没说过这句话\n举牌 aya大佬带带我",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.3.3",
    },
)


help_cmd = on_command("帮助", block=True, priority=12)


@help_cmd.handle()
async def _(bot : Bot = BotParam()):
    await help_cmd.finish("请在帮助文档中查看详细使用说明！（文档链接可在机器人简介或botmarket发布页获取）")


def create_matchers():
    def handler(meme: Meme) -> T_Handler:
        async def handle(
            matcher: Matcher, res: Union[str, BytesIO] = Depends(meme.func), bot: Bot = BotParam()
        ):
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            t = await bot.upload_file(("image.png",res.getvalue(),"image/jpeg"))
            await matcher.finish(MessageSegment.image(t))

        return handle

    for meme in memes:
        on_message(
            regex(meme.pattern),
            block=False,
            priority=12,
        ).append_handler(handler(meme))


create_matchers()
