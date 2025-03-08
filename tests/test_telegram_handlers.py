import pytest
from telegram_handlers import subscribe_handler, unsubscribe_handler, vars
from types import SimpleNamespace

# Create a dummy message object to simulate Telegram's message.
class DummyMessage:
    def __init__(self, text, user_id, chat_id):
        self.text = text
        self.from_user = SimpleNamespace(id=user_id)
        self.chat = SimpleNamespace(id=chat_id)
        self.answers = []
        self.reactions = []

    async def answer(self, text):
        self.answers.append(text)

    async def react(self, reaction):
        self.reactions.append(reaction)

@pytest.mark.asyncio
async def test_subscribe_unsubscribe():
    # Ensure a clean state for subscribers.
    vars.subscribers.clear()

    # Simulate sending a /subscribe command.
    dummy_subscribe = DummyMessage("/subscribe", 100, 100)
    await subscribe_handler(dummy_subscribe)
    assert 100 in vars.subscribers

    # Now simulate sending a /unsubscribe command.
    dummy_unsubscribe = DummyMessage("/unsubscribe", 100, 100)
    await unsubscribe_handler(dummy_unsubscribe)
    assert 100 not in vars.subscribers
