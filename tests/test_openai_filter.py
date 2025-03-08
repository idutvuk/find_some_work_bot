import pytest
from openai_filter import filter_is_job_offer, filter_match

# Dummy response to simulate OpenAI API call results.
class DummyResponse:
    def __init__(self, content):
        # Simulate the structure: response.choices[0].message.content
        self.choices = [type("DummyChoice", (), {"message": type("DummyMessage", (), {"content": content})})]

# Dummy async functions to simulate API responses.
async def dummy_create_success_job_offer(*args, **kwargs):
    return DummyResponse("1")

async def dummy_create_success_not_job_offer(*args, **kwargs):
    return DummyResponse("0")

async def dummy_create_success_match(*args, **kwargs):
    # Simulate scores for filters (e.g., "5 3 0")
    return DummyResponse("5 3 0")

@pytest.mark.asyncio
async def test_filter_is_job_offer_true(monkeypatch):
    # Monkeypatch the OpenAI API call in filter_is_job_offer.
    # monkeypatch.setattr("openai_filter.client.chat.completions.create", dummy_create_success_job_offer)
    result = await filter_is_job_offer("Я ПРИГЛАШАЮ ВСЕХ НА РАБОТУ В UNREAL ENGINE, БЛЕНДЕР МОДЕЛИРОВАНИЕ И РАЗРАБОТКУ ТЕЛЕГРАМ БОТОВ 🎉 ДА И ВООБЩЕ ОЦЕНИТЕ ЭТУ ГРУППУ ТАК ВЫСОКО КАК ТОЛЬКО ВОЗМОЖНО")
    assert result is True

@pytest.mark.asyncio
async def test_filter_is_job_offer_false(monkeypatch):
    # Monkeypatch to simulate a non-job offer response.
    # monkeypatch.setattr("openai_filter.client.chat.completions.create", dummy_create_success_not_job_offer)
    result = await filter_is_job_offer("с 8 марта всех банано-кошечек!! ❤️")
    assert result is False

# @pytest.mark.asyncio
# async def test_filter_match(monkeypatch):
#     # Monkeypatch for matching function.
#     # monkeypatch.setattr("openai_filter.client.chat.completions.create", dummy_create_success_match)
#     result = await filter_match("Test job offer text")
#     # Expected result: a list of scores as strings.
#     assert result == ["5", "3", "0"]
