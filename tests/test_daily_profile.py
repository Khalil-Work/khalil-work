"""Check external-data boundaries, fallback dates, and event-time arithmetic."""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location("daily", Path(__file__).parents[1] / "tools/refresh_daily_profile.py")
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)


class DailyProfileTests(unittest.TestCase):
    def test_event_timezone_boundaries_deduplication_and_filtering(self):
        now = datetime(2026, 10, 25, 16, tzinfo=timezone.utc)
        events = []
        for i, stamp in enumerate(["2026-10-24T22:00:00Z", "2026-10-25T04:00:00Z", "2026-10-25T10:00:00Z", "2026-10-25T16:00:00Z"]):
            events.append({"id": str(i), "type": "PushEvent", "actor": {"login": "Khalil-Work"}, "created_at": stamp})
        events += [events[0], {**events[0], "id": "other", "actor": {"login": "someone-else"}},
                   {**events[0], "id": "old", "created_at": "2024-01-01T00:00:00Z"}]
        self.assertEqual(daily.push_timing(events, now)["counts"], dict(Morning=1, Afternoon=1, Evening=1, Night=1))

    def test_provider_failure_preserves_content_and_original_date(self):
        old = {"quote": {"date": "2026-10-24", "text": "Keep learning."}, "trivia": {"date": "2026-10-24"}, "timing": {"total": 7}}
        def unavailable(url):
            raise OSError("offline")
        result = daily.fetch_state(datetime(2026, 10, 25, tzinfo=timezone.utc), old, unavailable)
        self.assertEqual(result["quote"]["date"], "2026-10-24")
        self.assertEqual(result["timing"]["total"], 7)
        self.assertEqual(len(result["warnings"]), 3)

    def test_same_day_content_is_not_replaced_on_manual_rerun(self):
        old = {"quote": {"date": "2026-10-25"}, "trivia": {"date": "2026-10-25"}}
        called = []
        def fetch(url):
            called.append(url)
            return []
        daily.fetch_state(datetime(2026, 10, 25, tzinfo=timezone.utc), old, fetch)
        self.assertTrue(all("api.github.com" in url for url in called))

    def test_source_text_escaping_and_trivia_answer_consistency(self):
        t = daily.trivia_from({"response_code": 0, "results": [{"question": "A &amp; B < C?", "correct_answer": "Yes", "incorrect_answers": ["No", "Maybe", "Unknown"]}]}, "2026-10-25")
        self.assertIn(t["answer"], t["options"])
        image = daily.render_trivia(t, daily.PALETTES["dark"])
        root = ET.fromstring(image)
        self.assertIn("A & B < C?", "".join(root.itertext()))
        self.assertNotIn("<script", image)

    def test_error_and_oversized_quote_are_rejected(self):
        with self.assertRaises(ValueError):
            daily.quote_from([{"q": "Service unavailable", "a": "zenquotes.io"}], "2026-10-25")
        with self.assertRaises(ValueError):
            daily.quote_from([{"q": "word " * 26, "a": "Author"}], "2026-10-25")


if __name__ == "__main__":
    unittest.main()
