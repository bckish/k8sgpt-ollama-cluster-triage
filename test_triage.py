import json
import unittest
from pathlib import Path
from triage import analyze


class TriageTests(unittest.TestCase):
    def test_fixture(self):
        report = analyze(json.loads(Path("fixtures/events.json").read_text()))
        self.assertEqual(report["warnings"], 3)
        self.assertEqual(report["categories"], {"capacity": 1, "health": 1, "storage": 1})
        self.assertEqual(report["mode"], "read-only")

    def test_redacts_source_details(self):
        report = analyze({"items": [{"type":"Warning", "reason":"custom-private-name", "message":"secret-example"}]})
        self.assertNotIn("secret-example", json.dumps(report))
        self.assertNotIn("custom-private-name", json.dumps(report))
        self.assertEqual(report["categories"], {"unclassified": 1})

    def test_invalid_and_empty(self):
        with self.assertRaises(ValueError):
            analyze({})
        self.assertEqual(analyze({"items": []})["warnings"], 0)


if __name__ == "__main__":
    unittest.main()
