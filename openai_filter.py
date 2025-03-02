from openai import OpenAI

import logging
from variables import BotConfig

logger = logging.getLogger(__name__)
config = BotConfig()

client = OpenAI()


async def filter_match(post_text: str) -> list:
    """
    Использует OpenAI ChatCompletion API для определения, следует ли пересылать сообщение.
    """
    prompt = (
        """
        You are a filtering assistant helping a freelancer to list jobs. 
        input:
        Job offer post text;
        filters splitted by pipe symbol (|)
        output:
        Numbers showing how job offer post correlates to each filter from 0 to 5
        Example of output: 
        2 0 1 4
        
        
        Correlation example:
        <post>
        🚀 Looking for a Senior Django Developer to Build a Scalable Web App
        We are seeking an experienced Python developer with strong expertise in Django to help build a high-performance web application. The project involves working some basic tech stack
        </post>
        Python Django/FastAPI Developer	5
        Python developer	4
        REST API Development	1
        Programming	2
        Junior web developer	3
        Firefighting	0
        
        output:
        5 4 1 2 3 0
        """
        + f"Filters (split by | symbol):\n'{config.filter_query}'. "
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Post: {post_text}"},
            ],
            temperature=0.0,
        )
        answers = response.choices[0].message.content.split()
        logger.info(f"OpenAI filter response: {answers}")
        return answers

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return False
