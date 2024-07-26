from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot import logger
from nonebot.params import CommandArg, ArgPlainText
from nonebot import get_plugin_config

from .config import Config

plugin_name = "weather"
plugin_config = get_plugin_config(Config)
logger.info(f"{plugin_name} config: {plugin_config}")

try:
    command_priority = plugin_config.weather.command_priority
except AttributeError:
    command_priority = plugin_config.default_plugin_priority

async def is_enable() -> bool:
    return plugin_config.weather.plugin_enabled

weather = on_command("天气",
                    rule=is_enable,
                    force_whitespace=True, 
                    priority=command_priority
                    )

@weather.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("location", args)

@weather.got("location", prompt="请输入地名")
async def got_location(location: str = ArgPlainText()):
    if location not in ["北京", "上海", "广州", "深圳"]:
        await weather.reject(f"你想查询的城市 {location} 暂不支持，请重新输入！")
    await weather.finish(f"今天{location}的天气是...")