import subprocess
from pathlib import Path

from config import settings


def cut_audio_from_video(video_path: Path) -> Path:
    res_dir = settings.app.audio_dir
    m4a_path = res_dir / video_path.with_suffix('.m4a').name
    wav_path = res_dir / video_path.with_suffix('.wav').name

    subprocess.run(
        [
            'ffmpeg',
            '-y',
            '-i',
            video_path.as_posix(),
            '-vn',
            '-c:a',
            'copy',
            m4a_path,
        ],
        check=True,
    )

    subprocess.run(
        [
            'faad',
            '-o',
            wav_path.as_posix(),
            m4a_path.as_posix(),
        ],
        check=True,
    )
    return wav_path


def cut_audios_from_videos(videos_dir: Path) -> list[Path]:
    for video_file_path in videos_dir.iterdir():
        p = Path(video_file_path)
        cut_audio_from_video(p)
