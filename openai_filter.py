from openai import OpenAI

import logging
from variables import Variables

logger = logging.getLogger(__name__)
vars = Variables()

client = OpenAI()

async def filter_is_job_offer(post_text: str) -> bool:
    prompt = (
        """
        Is this post a job offer or freelance order or paid help request? Answer 1 for yes, 0 for no
        """
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Post: {post_text}"},
            ],
            temperature=0.0,
            max_tokens=5
        )
        answer = response.choices[0].message.content == '1'
        logger.info(f"isJobOffer response: {answer}")
        return answer

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return False


async def filter_match(post_text: str) -> list:
    prompt = (
        """
        You are a highly qualified expert in text analysis and automated job matching. Your task is to evaluate a job offer or order post against a given technology stack.
        Input:
            Post (string): A text describing a job offer or order.
            Filters (string/array): A list of keywords or phrases (technologies/skills), separated by commas or provided as an array.
        Task:
        For each filter, assign a score from 0 to 5 based on its relevance to the post, where:
            0 means no mention or relevance;
            5 means a full match with explicit mention.
        Consider direct mentions, synonyms, abbreviations, context, frequency, and overall appropriateness (e.g., a post seeking a 3D designer might score "Interior Visualizer" as 3/5).
        Output:
        Return a space-separated string of scores matching the order of the filters. If the post is not a job offer or order, return "0".
        """
        + f"Filters:\n'{vars.filters}'. "
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
        logger.info(f"response: {answers}")
        return answers

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return ["0"]
