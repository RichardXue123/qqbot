import nonebot
from nonebot.adapters.onebot.v11 import Adapter as V11Adapter
from nonebot.adapters.onebot.v12 import Adapter as V12Adapter
from nonebot.adapters.console import Adapter as ConsoleAdapter

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)
driver.register_adapter(V12Adapter)
driver.register_adapter(ConsoleAdapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
# nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
nonebot.load_plugins("src/plugins")  # 本地插件

if __name__ == "__main__":
    nonebot.run()