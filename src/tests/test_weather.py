from datetime import datetime

import pytest
from nonebug import App
from nonebot.adapters.console import User, Message, MessageEvent
from nonebot import require

def make_event(message: str) -> MessageEvent:
    return MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message(message),
        user=User(id="user"),
    )

@pytest.mark.asyncio
async def test_weather(app: App):
    from src.plugins.weather import weather
    event = MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message("/天气 北京"),
        user=User(id="user"),
    )
    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "今天北京的天气是...", result=None)
        ctx.should_finished(weather)

    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()
        event = make_event("/天气 南京")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "你想查询的城市 南京 暂不支持，请重新输入！", result=None)
        ctx.should_rejected(weather)

        event = make_event("北京")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "今天北京的天气是...", result=None)
        ctx.should_finished(weather)