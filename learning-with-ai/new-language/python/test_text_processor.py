import unittest
from text_processor import TextProcessor, TextAnalysisReport

class TestTextProcessorMiniProject(unittest.TestCase):
    def setUp(self):
        self.sample_text = (
            "Artificial Intelligence is transforming software development. "
            "Developers use AI tools to learn new programming languages, "
            "write tests, and refactor complex code efficiently."
        )

    def test_clean_and_tokenize(self):
        tokens = TextProcessor.clean_and_tokenize("Hello, World! Welcome to Python.")
        self.assertEqual(tokens, ["hello", "world", "welcome", "to", "python"])

    def test_empty_string_tokenization(self):
        self.assertEqual(TextProcessor.clean_and_tokenize(""), [])
        self.assertEqual(TextProcessor.clean_and_tokenize(None), [])

    def test_frequency_analysis_filtering(self):
        tokens = ["ai", "python", "the", "ai", "code", "the", "ai"]
        freqs = TextProcessor.analyze_frequencies(tokens, top_n=2)
        # 'the' is a stop-word and should be omitted
        self.assertEqual(freqs, [("ai", 3), ("python", 1)])

    def test_full_report_generation(self):
        report = TextProcessor.generate_report(self.sample_text, words_per_minute=100)
        self.assertIsInstance(report, TextAnalysisReport)
        self.assertGreater(report.total_words, 10)
        self.assertGreater(report.unique_words, 5)
        self.assertGreater(report.reading_time_seconds, 0.0)
        
        report_dict = report.to_dict()
        self.assertIn("total_words", report_dict)
        self.assertIn("top_frequencies", report_dict)

if __name__ == "__main__":
    unittest.main()
