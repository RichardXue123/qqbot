from pydantic import BaseModel
from nonebot import get_plugin_config

class ScopedConfig(BaseModel):
    api_key: str
    plugin_enabled: bool = True

class Config(BaseModel):
    default_plugin_priority: int = 10
    weather: ScopedConfig


if __name__ == "__main__":
    config = get_plugin_config(Config)
    print(config.json())