from openai import OpenAI

import logging
from variables import BotConfig

logger = logging.getLogger(__name__)
config = BotConfig()

client = OpenAI()


async def should_forward(post_text: str) -> bool:
    """
    Использует OpenAI ChatCompletion API для определения, следует ли пересылать сообщение.
    """
    prompt = (
        f"You are a filtering assistant helping a freelancer to list jobs. "
        f"Determine if the following post may be an offer partially related to the filter based on the filter strength of {config.filter_strength}/5. "
        f"Answer only with 'Yes' or 'No'. "
        f"Filter: '{config.filter_query}'. "
    )
    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f'Post: {post_text}'}
        ],
        temperature=0.0,
        max_tokens=5,
        frequency_penalty=1.0 - (config.filter_strength / 5))
        answer = response.choices[0].message.content.strip().lower()
        logger.info(f"OpenAI filter response: {answer}")
        return answer.startswith("yes")
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return False
