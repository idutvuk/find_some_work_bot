import pytest
from telegram_handlers import subscribe_handler, unsubscribe_handler, v
from types import SimpleNamespace

# Create dummy
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
    # no subscribers.
    v.subscribers.clear()

    dummy_subscribe = DummyMessage("/subscribe", 100, 100)
    await subscribe_handler(dummy_subscribe)
    assert 100 in v.subscribers

    dummy_unsubscribe = DummyMessage("/unsubscribe", 100, 100)
    await unsubscribe_handler(dummy_unsubscribe)
    assert 100 not in v.subscribers
