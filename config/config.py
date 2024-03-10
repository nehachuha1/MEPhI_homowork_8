from dataclasses import dataclass
from dotenv import dotenv_values

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    TgBot: TgBot

def get_env_values(path: str | None = None) -> Config:
    env_values = dotenv_values(path)
    return Config(TgBot=TgBot(token=env_values['TOKEN']))