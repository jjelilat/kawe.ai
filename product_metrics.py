"""Small, dependency-free helpers for Kàwé product limits and summary UI."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil


MAX_UPLOAD_BYTES = 20 * 1024 * 1024
WORDS_PER_MINUTE = 150


@dataclass(frozen=True)
class SummaryMetrics:
    source_words: int
    summary_words: int
    compression_percentage: int
    estimated_listening_minutes: int


def validate_upload_size(size_bytes: int, max_bytes: int = MAX_UPLOAD_BYTES) -> None:
    """Raise a helpful error before an oversized upload is processed."""
    if size_bytes < 0:
        raise ValueError("Upload size cannot be negative.")
    if size_bytes > max_bytes:
        max_megabytes = max_bytes // (1024 * 1024)
        raise ValueError(f"This file is too large. Upload a file up to {max_megabytes} MB.")


def build_summary_metrics(source_words: int, summary_text: str) -> SummaryMetrics:
    """Return useful, provider-independent information about a summary."""
    if source_words < 0:
        raise ValueError("Source word count cannot be negative.")

    summary_words = len(summary_text.split())
    compression_percentage = (
        round((summary_words / source_words) * 100) if source_words else 0
    )
    listening_minutes = ceil(summary_words / WORDS_PER_MINUTE) if summary_words else 0

    return SummaryMetrics(
        source_words=source_words,
        summary_words=summary_words,
        compression_percentage=compression_percentage,
        estimated_listening_minutes=listening_minutes,
    )
