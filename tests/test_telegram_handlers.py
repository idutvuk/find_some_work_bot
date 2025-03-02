import pytest
from telegram_handlers import subscribe_handler, unsubscribe_handler
from variables import Variables

# Create a dummy message class to simulate an aiogram message.
class DummyMessage:
    def __init__(self, user_id, text=""):
        self.from_user = type("User", (), {"id": user_id})
        self.text = text
        self._responses = []

    async def answer(self, text):
        self._responses.append(text)

@pytest.fixture
def dummy_config(monkeypatch):
    # Ensure we have a clean config for testing
    vars = Variables()
    vars.subscribers = set()
    monkeypatch.setattr("telegram_handlers.config", vars)
    return vars

@pytest.mark.asyncio
async def test_subscribe_handler(dummy_config):
    dummy_message = DummyMessage(user_id=111)
    await subscribe_handler(dummy_message)
    # Check that the response was sent
    assert "subscribed" in dummy_message._responses[-1].lower()
    # Check that the user was added to subscribers
    assert 111 in dummy_config.subscribers

@pytest.mark.asyncio
async def test_unsubscribe_handler(dummy_config):
    # Pre-add a subscriber.
    dummy_config.subscribers.add(222)
    dummy_message = DummyMessage(user_id=222)
    await unsubscribe_handler(dummy_message)
    # Check that the response was sent
    assert "unsubscribed" in dummy_message._responses[-1].lower()
    # Check that the user was removed from subscribers
    assert 222 not in dummy_config.subscribers
