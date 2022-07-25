import json

import nonebot
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter
from aiohttp import ClientSession

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(KaiheilaAdapter)

nonebot.load_from_toml("pyproject.toml")
nonebot.run()