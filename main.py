from pathlib import Path

from config import settings
from proccesings.ai_proccessing import generate_summaries
from proccesings.video_proccessing import cut_audios_from_videos
from proccesings.whisperx_proccessing import transcribe_audios_with_whisperx


def main():
    cut_audios_from_videos(settings.app.video_dir)

    transcribe_audios_with_whisperx(settings.app.audio_dir)

    generate_summaries(settings.app.trns_dir)


if __name__ == '__main__':
    main()
