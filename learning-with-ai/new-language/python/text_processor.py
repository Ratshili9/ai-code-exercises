"""
Module: Learning a New Programming Language - Text Processing Mini-Project
Demonstrating structured component architecture, type safety, error boundaries,
and algorithmic text analysis learned through the AI-guided 4-step pattern.
"""
from typing import List, Dict, Tuple
import re
from collections import Counter


class TextAnalysisReport:
    """Represents the structured result of an analyzed text corpus."""
    def __init__(self, total_words: int, unique_words: int, top_frequencies: List[Tuple[str, int]], reading_time_seconds: float):
        self.total_words = total_words
        self.unique_words = unique_words
        self.top_frequencies = top_frequencies
        self.reading_time_seconds = reading_time_seconds

    def to_dict(self) -> Dict[str, object]:
        return {
            "total_words": self.total_words,
            "unique_words": self.unique_words,
            "top_frequencies": self.top_frequencies,
            "reading_time_seconds": self.reading_time_seconds
        }


class TextProcessor:
    """Text processing engine implementing tokenization, stop-word filtering, and frequency analysis."""
    STOP_WORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "is", "it", "of", "as"}

    @classmethod
    def clean_and_tokenize(cls, text: str) -> List[str]:
        """Sanitize text by stripping non-alphanumeric characters and splitting into tokens."""
        if not text or not isinstance(text, str):
            return []
        cleaned = re.sub(r"[^\w\s]", "", text.lower())
        return [token for token in cleaned.split() if token]

    @classmethod
    def analyze_frequencies(cls, tokens: List[str], top_n: int = 5) -> List[Tuple[str, int]]:
        """Calculate word frequency counts excluding common stop-words."""
        filtered = [t for t in tokens if t not in cls.STOP_WORDS]
        counts = Counter(filtered)
        return counts.most_common(top_n)

    @classmethod
    def generate_report(cls, text: str, words_per_minute: int = 200) -> TextAnalysisReport:
        """Generate comprehensive metrics and estimated reading time for a text block."""
        tokens = cls.clean_and_tokenize(text)
        total_count = len(tokens)
        unique_count = len(set(tokens))
        top_freq = cls.analyze_frequencies(tokens)
        reading_time = round((total_count / words_per_minute) * 60, 2) if total_count > 0 else 0.0

        return TextAnalysisReport(
            total_words=total_count,
            unique_words=unique_count,
            top_frequencies=top_freq,
            reading_time_seconds=reading_time
        )
