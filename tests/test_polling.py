import pytest
from telethon_polling import poll_channels, vars, telethon_client

# Dummy message to simulate Telegram messages.
class DummyMessage:
    def __init__(self, message, id):
        self.message = message
        self.id = id

# Dummy bot that collects sent messages.
class DummyBot:
    def __init__(self):
        self.sent_messages = []

    async def send_message(self, chat_id, text, disable_web_page_preview):
        self.sent_messages.append((chat_id, text))

@pytest.mark.asyncio
async def test_poll_channels(monkeypatch):
    # Simulate telethon_client.get_messages to return a dummy message.
    async def dummy_get_messages(channel, limit):
        return [DummyMessage("Test job offer text", 10)]
    monkeypatch.setattr(telethon_client, "get_messages", dummy_get_messages)
    
    # Monkeypatch the filter functions in telethon_polling.
    async def dummy_filter_is_job_offer(text):
        return True
    async def dummy_filter_match(text):
        return ["5"]  # Passes the filter if 5 >= filter_strength.
    monkeypatch.setattr("telethon_polling.filter_is_job_offer", dummy_filter_is_job_offer)
    monkeypatch.setattr("telethon_polling.filter_match", dummy_filter_match)
    
    # Setup dummy bot and configure variables.
    dummy_bot = DummyBot()
    vars.channels.clear()
    vars.channels["dummy_channel"] = 0
    vars.subscribers.clear()
    vars.subscribers.add(123)
    vars.filter_strength = 3
    vars.filters = ["dummy_filter"]
    vars.post_preview = True

    await poll_channels(dummy_bot, [("dummy_channel", 0)])
    
    # Verify that a message was sent to at least one subscriber.
    assert len(dummy_bot.sent_messages) > 0
