import json
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
                self.post_preview: bool = data.get("post_preview", True)
        except FileNotFoundError:
            logger.error("load_variables error - file not found")
        
    def save_variables(self):
        data = {
            "filter_strength": self.filter_strength,
            "filters": self.filters,
            "parse_mode": self.parse_mode,
            "subscribers": list(self.subscribers),
            "channels": self.channels,
            "post_preview": self.post_preview
        }
        with open("variables.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    
    def __init__(self):
        self.load_variables()

