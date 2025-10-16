import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    base_dir: Path = Path(__file__).parent
    content_dir: Path = base_dir / 'content'
    video_dir: Path = content_dir / '0_videos'
    audio_dir: Path = content_dir / '1_audios'
    trns_dir: Path = content_dir / '2_transcriptions'
    smrz_dir: Path = content_dir / '3_summarizations'
    whisperx_model: str = 'large-v2'


class Settings(BaseSettings):
    # без значения по умолчанию, чтобы ошибка была явной, если ключ не найден
    OPENAI_API_KEY: str = ''
    app: AppSettings = AppSettings()

    # .env.default читается первым, затем .env имеет приоритет
    model_config = SettingsConfigDict(
        env_file=('.env.default', '.env'),
        env_nested_delimiter='__',
    )


settings = Settings()

os.environ.setdefault(
    'OPENAI_API_KEY',
    settings.OPENAI_API_KEY,
)
