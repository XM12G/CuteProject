import re
import shlex
from typing import List, Optional

from nonebot.rule import Rule
from nonebot import get_driver
from nonebot.typing import T_State
from nonebot.params import State, Depends
from nonebot.adapters.kaiheila import MessageSegment
from nonebot.adapters.kaiheila.event import MessageEvent

ARG_KEY = "ARG"
ARGS_KEY = "ARGS"
REGEX_DICT = "REGEX_DICT"
REGEX_GROUP = "REGEX_GROUP"
REGEX_ARG = "REGEX_ARG"
def unescape(s: str) -> str:
    """
    :说明:

      对字符串进行 CQ 码去转义。

    :参数:

      * ``s: str``: 需要转义的字符串
    """
    return (
        s.replace("&#44;", ",")
        .replace("&#91;", "[")
        .replace("&#93;", "]")
        .replace("&amp;", "&")
    )

def regex(pattern: str) -> Rule:
    def checker(event: MessageEvent, state: T_State = State()) -> bool:
        msg = event.get_message()
        msg_seg: MessageSegment = msg[0]
        if not msg_seg.is_text():
            return False

        seg_text = str(msg_seg).lstrip()
        start = "|".join(get_driver().config.command_start)
        matched = re.match(rf"(?:{start})(?:{pattern})", seg_text, re.IGNORECASE | re.S)
        if not matched:
            return False

        new_msg = msg.copy()
        seg_text = seg_text[matched.end() :].lstrip()
        if seg_text:
            new_msg[0].data["text"] = seg_text
        else:
            new_msg.pop(0)
        state[REGEX_DICT] = matched.groupdict()
        state[REGEX_GROUP] = matched.groups()
        state[REGEX_ARG] = new_msg

        msg_text = new_msg.extract_plain_text()
        state[ARG_KEY] = unescape(msg_text).strip()
        args: List[str] = []
        try:
            texts = shlex.split(msg_text)
        except:
            texts = msg_text.split()
        for text in texts:
            text = unescape(text).strip()
            if text:
                args.append(text)
        state[ARGS_KEY] = args

        return True

    return Rule(checker)


def Args(num: Optional[int] = None):
    async def dependency(state: T_State = State()):
        args: List[str] = state[ARGS_KEY]
        if num is not None and len(args) != num:
            return
        return args

    return Depends(dependency)


def RegexArg(key: str):
    async def dependency(state: T_State = State()):
        args: dict = state[REGEX_DICT]
        return args.get(key, None)

    return Depends(dependency)


def RegexArgs(num: Optional[int] = None):
    async def dependency(state: T_State = State()):
        args: List[str] = list(state[REGEX_GROUP])
        if num is not None and len(args) != num:
            return
        return args

    return Depends(dependency)


def Arg():
    async def dependency(state: T_State = State()):
        arg: str = state[ARG_KEY]
        if arg:
            return arg

    return Depends(dependency)


def NoArg():
    async def dependency(args: List[str] = Args(0)):
        return

    return Depends(dependency)
