from pathlib import Path

from openai import api_key
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

from config import settings

USER_PROMPT = """\
Ты — эксперт по анализу и сжатию знаний из учебных видео. Твоя задача — создать подробное, структурированное и логически выстроенное саммари по транскрипции видеоурока выдающегося преподавателя, у которого следует перенять как можно больше опыта.

Инструкция:
1. Внимательно проанализируй текстовую транскрипцию.
2. Не опускай никаких ценных моментов, советов, мыслей, примеров, даже если они кажутся незначительными.
3. Учитывай контекст: автор — профессионал, и каждая мелочь имеет обучающую ценность.
4. Если в тексте есть примеры, уточнения, сравнения или личные наблюдения автора — включи их в саммари.
5. Если автор делает практические рекомендации или пошаговые действия — выдели их как отдельные пункты.
6. Сохрани при этом краткость формулировок, но не теряй смысл ни одной детали.

Формат вывода (в Markdown):

# Саммари видеоурока: {topic}

## 1. Практические советы и методы
(Все конкретные рекомендации, техники, пошаговые алгоритмы и приёмы, предложенные автором)

## 2. Важные детали и наблюдения
(Дополнительные тонкости, предостережения, нюансы, оговорки, которые помогают глубже понять материал)

## 3. Выводы и ключевые инсайты
(Главные уроки, которые стоит вынести и применить на практике)

Каждый пункт должен содержать подзаголовки, списки и ясные структурные деления, чтобы читатель мог быстро воспринять материал и повторно использовать его как обучающую конспект-карту.

Требование:
- Ясность ≠ упрощение. Не искажай смысл.
- Не добавляй информации, которой нет в тексте.
- Используй язык оригинала транскрипции (если это русский — пиши по-русски).

---
ТЕКСТ ТРАСНКРИПЦИИ УРОКА:
{lesson_text}
"""


def ask_agent(question: str) -> str:
    agent = Agent(
        model='openai:gpt-5-nano',
        instructions='Always answer in Russian.',
    )

    result = agent.run_sync(question)

    return result.output


def generate_summaries(texts_dir: Path):
    for text_file_path in texts_dir.iterdir():
        t = Path(text_file_path)

        with open(text_file_path.as_posix(), 'rt', encoding='utf-8') as f:
            text = f.read()
            topic = text_file_path.stem.split('1234567890. ')

            prompt = USER_PROMPT.format(topic=topic, lesson_text=text)

            model_answer = ask_agent(prompt)

            summary_file_path = (
                settings.app.smrz_dir / text_file_path.with_suffix('.md').name
            )

        with open(summary_file_path, 'wt', encoding='utf-8') as f_sum:
            f_sum.write(model_answer)
