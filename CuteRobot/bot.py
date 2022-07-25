import nonebot
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter
nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(KaiheilaAdapter)

nonebot.load_plugins("cuterobot/plugins")
nonebot.run()