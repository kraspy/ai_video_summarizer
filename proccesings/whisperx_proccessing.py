import gc
import warnings
from pathlib import Path

import torch
import whisperx

from config import settings

warnings.filterwarnings(
    'ignore',
    message='.*TensorFloat-32 \\(TF32\\) has been disabled.*',
    module='pyannote\\.audio.*',
)

warnings.filterwarnings(
    'ignore',
    category=DeprecationWarning,
)


def transcribe_audio_with_whisperx(audio_path: Path) -> None:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    compute_type = 'float16' if device == 'cuda' else 'int8'

    model_wx = whisperx.load_model(
        settings.app.whisperx_model,
        device=device,
        compute_type=compute_type,
    )
    audio_data = whisperx.load_audio(str(audio_path.as_posix()))

    result_transcription = model_wx.transcribe(
        audio_data,
        language='ru',
        batch_size=5,
    )

    align_model, align_metadata = whisperx.load_align_model(
        language_code=result_transcription['language'], device=device
    )
    aligned_result = whisperx.align(
        result_transcription['segments'],
        align_model,
        align_metadata,
        audio_data,
        device=device,
        return_char_alignments=False,
    )

    del align_model
    gc.collect()
    if device == 'cuda':
        torch.cuda.empty_cache()

    result = []

    for seg in aligned_result.get('segments', []):
        seg_text = (seg.get('text') or '').strip()

        result.append(seg_text)
    result_text = ' '.join([text for text in result])

    result_text_file_path = settings.app.trns_dir / audio_path.with_suffix('.txt').name

    with open(result_text_file_path, 'wt', encoding='utf-8') as f:
        f.write(result_text)


def transcribe_audios_with_whisperx(audios_dir: Path) -> None:
    for audio_file_path in audios_dir.iterdir():
        if audio_file_path.suffix == '.wav':
            p = Path(audio_file_path)
            transcribe_audio_with_whisperx(p)
