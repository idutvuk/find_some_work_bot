import json
import functools
import logging
import asyncio

logger = logging.getLogger(__name__)


class BotConfig:
    def load_variables(self):
        try:
            with open("variables.json", "r") as f:
                data = json.load(f)
                self.filter_query: str = data.get("filter_query", "job offer")
                self.filter_strength: int = data.get("filter_strength", 3)
                self.subscribers: set = set(data.get("subscribers", []))
                self.channels: list = data.get("channels", {})
        except FileNotFoundError:
            pass
        
    def save_variables(self, _ = ()):
        data = {
            "filter_query": self.filter_query,
            "filter_strength": self.filter_strength,
            "subscribers": list(self.subscribers),
            "channels": self.channels
        }
        with open("variables.json", "w") as f:
            json.dump(data, f, indent=4)
            logger.info("saved")
    
    
    def __init__(self):
        self.load_variables()


    def use_var(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs) 
            self.save_variables(result)
            return result
        return wrapper
