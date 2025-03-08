import pytest
from openai_filter import filter_is_job_offer, filter_match


@pytest.mark.asyncio
async def test_filter_is_job_offer_false():
    result = await filter_is_job_offer("THIS IS NOT JOB OFFER TEST. THIS IS FOR MOCKING")
    assert result is False

@pytest.mark.asyncio
async def test_filter_match():
    result = await filter_match("Test job offer text")
    assert result == ["0"]
