from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText
from nonebot import CommandGroup

help_group = CommandGroup("help", prefix_aliases=True, force_whitespace=True)
help = help_group.command(tuple())
help_help = help_group.command("help")

@help.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("command", args)

@help.got("command", prompt="请输入指令")
async def got_command(command: str = ArgPlainText()):
    if command == "help":
        await help.finish("帮助文档")
    else:
        await help.finish(f"未找到指令 {command}")

@help_help.handle()
async def handle_function(matcher: Matcher):
    await help_help.finish("帮助文档")

