import json
import functools
import logging

logger = logging.getLogger(__name__)


class Variables:
    def load_variables(self):
        try:
            with open("variables.json", "r") as f:
                data = json.load(f)
                self.filters: list = data.get("filters", ["job offer"])
                self.filter_strength: int = data.get("filter_strength", 3)
                self.subscribers: set = set(data.get("subscribers", []))
                self.channels: dict = data.get("channels", {})
                self.parse_mode: str = data.get("parse_mode", "list")
        except FileNotFoundError:
            logger.error("load_variables error - file not found")
        
    def save_variables(self):
        data = {
            "filter_strength": self.filter_strength,
            "filters": self.filters,
            "parse_mode": self.parse_mode,
            "subscribers": list(self.subscribers),
            "channels": self.channels
        }
        with open("variables.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    
    def __init__(self):
        self.load_variables()


    def use_var(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs) 
            self.save_variables(result)
            return result
        return wrapper
