from datetime import datetime

import pytest
from nonebug import App
from nonebot.adapters.onebot.v12 import Message, MessageSegment, MessageEvent
from nonebot import rule

def make_event(message: str) -> MessageEvent:
    message_json = {
        "id": "b6e65187-5ac0-489c-b431-53078e9d2bbb",
        "self": {
            "platform": "qq",
            "user_id": "123234"
        },
        "time": datetime.now().timestamp(),
        "type": "message",
        "detail_type": "private",
        "sub_type": "",
        "message_id": "6283",
        "message": [
            {
                "type": "text",
                "data": {
                    "text": message
                }
            }
        ],
        "alt_message": message,
        "user_id": "123456788",
        "qq.nickname": "海阔天空"
    }
    return MessageEvent.parse_obj(message_json)



@pytest.mark.asyncio
async def test_weather(app: App):
    from src.plugins.weather import weather
    event = make_event("/天气 北京")
    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_pass_rule()
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

if __name__ == "__main__":
    make_event("test")