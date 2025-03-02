import pytest
from openai_filter import filter_match

# We will mock the openai.ChatCompletion.create function.
@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    class DummyResponse:
        def __init__(self, answer):
            self.choices = [type("Choice", (), {"message": {"content": answer}})]

    async def dummy_should_forward(*args, **kwargs):
        # You can toggle the answer to "Yes" or "No" to test both scenarios.
        return DummyResponse("Yes")

    def dummy_create(*args, **kwargs):
        return dummy_should_forward()

    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)

@pytest.mark.asyncio
async def test_should_forward_yes():
    # Provide a sample post_text.
    result = await filter_match("This is a job offer post.")
    # The dummy always returns an answer starting with "yes"
    assert result is True

@pytest.mark.asyncio
async def test_should_forward_no(monkeypatch):
    # Modify the dummy function to return "No"
    class DummyResponse:
        def __init__(self, answer):
            self.choices = [type("Choice", (), {"message": {"content": answer}})]
    def dummy_create(*args, **kwargs):
        return type("Dummy", (), {"choices": [type("Choice", (), {"message": {"content": "No"}})]})
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_create)

    result = await filter_match("This is a job offer post.")
    assert result is False
