"""Dataset loading: every source is mapped to a common {audio array, text} format at 16 kHz."""

import io
from dataclasses import dataclass

import numpy as np
import soundfile as sf
import soxr
from datasets import Audio, Dataset, concatenate_datasets, load_dataset

SAMPLING_RATE = 16_000


@dataclass(frozen=True)
class Source:
    repo: str
    text_column: str = "text"
    # Optional (column, value) filter, e.g. keep only the Souss (Tachelhit) accent.
    filter_column: str | None = None
    filter_value: str | None = None


SOURCES: dict[str, Source] = {
    # ~15 h of Tachelhit from subtitled films; text is an Arabic translation. Apache-2.0.
    "dahimi": Source("SoufianeDahimi/Tamazight-ASR-Dataset-v2"),
    # Crowdsourced Moroccan Tamazight with Arabic translations; keep Souss speakers. CC-BY-4.0.
    "tutlait_souss": Source("Ma-OpenHub/Tutlait-v1", filter_column="accent", filter_value="souss"),
}


def decode_audio(audio: dict) -> np.ndarray:
    """Decode raw audio bytes to mono float32 at 16 kHz (avoids the torchcodec/FFmpeg dependency)."""
    if audio.get("bytes"):
        array, sr = sf.read(io.BytesIO(audio["bytes"]), dtype="float32")
    else:
        array, sr = sf.read(audio["path"], dtype="float32")
    if array.ndim > 1:
        array = array.mean(axis=1)
    if sr != SAMPLING_RATE:
        array = soxr.resample(array, sr, SAMPLING_RATE)
    return array


def load_source(name: str, split: str, max_samples: int | None = None) -> Dataset:
    src = SOURCES[name]
    ds = load_dataset(src.repo, split=split)
    if src.filter_column:
        ds = ds.filter(lambda v: v == src.filter_value, input_columns=src.filter_column)
    if max_samples:
        ds = ds.select(range(min(max_samples, len(ds))))
    ds = ds.cast_column("audio", Audio(decode=False))
    if src.text_column != "text":
        ds = ds.rename_column(src.text_column, "text")
    ds = ds.select_columns(["audio", "text"])
    return ds.add_column("source", [name] * len(ds))


def load_mixture(names: list[str], split: str, max_samples: int | None = None) -> Dataset:
    return concatenate_datasets([load_source(n, split, max_samples) for n in names])
