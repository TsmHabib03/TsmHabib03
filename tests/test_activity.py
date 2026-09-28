"""Checks that contribution graphics cannot silently publish incomplete or invented totals."""
from argparse import Namespace
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import update_activity as activity


def sample_calendar():
    start = date(2025, 1, 1)
    days = []
    for i in range(365):
        count = 1 if i == 0 else 7 if i == 364 else 0
        days.append({"date": (start + timedelta(days=i)).isoformat(), "contributionCount": count,
                     "contributionLevel": "FIRST_QUARTILE" if count else "NONE"})
    return {"totalContributions": 8, "weeks": [{"contributionDays": days[i:i+7]} for i in range(0, 365, 7)]}


class CalendarIntegrity(unittest.TestCase):
    def setUp(self):
        self.calendar = sample_calendar()
        self.today = date(2025, 12, 31)

    def test_complete_calendar_and_totals(self):
        result = activity.normalize_calendar(self.calendar, self.today)
        self.assertEqual(result["total"], 8)
        self.assertEqual(len(result["days"]), 365)
        self.assertEqual(sum(day["count"] > 0 for day in result["days"]), 2)

    def test_rejects_inflated_total(self):
        self.calendar["totalContributions"] = 999
        with self.assertRaisesRegex(ValueError, "total"):
            activity.normalize_calendar(self.calendar, self.today)

    def test_rejects_missing_or_duplicate_day(self):
        self.calendar["weeks"][0]["contributionDays"][1] = deepcopy(self.calendar["weeks"][0]["contributionDays"][0])
        with self.assertRaisesRegex(ValueError, "duplicate or missing"):
            activity.normalize_calendar(self.calendar, self.today)

    def test_rejects_incomplete_and_stale_year(self):
        broken = deepcopy(self.calendar)
        broken["weeks"].pop()
        with self.assertRaisesRegex(ValueError, "complete"):
            activity.normalize_calendar(broken, self.today)
        with self.assertRaisesRegex(ValueError, "stale"):
            activity.normalize_calendar(self.calendar, self.today + timedelta(days=3))

    def test_rejects_negative_counts_and_unknown_levels(self):
        broken = deepcopy(self.calendar)
        broken["weeks"][0]["contributionDays"][0]["contributionCount"] = -1
        with self.assertRaisesRegex(ValueError, "count"):
            activity.normalize_calendar(broken, self.today)
        self.calendar["weeks"][0]["contributionDays"][0]["contributionLevel"] = "UNRECOGNIZED"
        with self.assertRaises(ValueError):
            activity.normalize_calendar(self.calendar, self.today)

    def test_both_graphs_preserve_every_actual_date_once(self):
        data = activity.normalize_calendar(self.calendar, self.today)
        data.update(username="fixture", updated=self.today.isoformat())
        for mobile in (False, True):
            root = ET.fromstring(activity.render_activity(data, mobile))
            cells = root.findall(".//{http://www.w3.org/2000/svg}g/{http://www.w3.org/2000/svg}title")
            dates = [cell.text.split(":")[0] for cell in cells]
            self.assertEqual(len(dates), 365)
            self.assertEqual(set(dates), {day["date"] for day in data["days"]})

    def test_network_failure_does_not_replace_existing_artwork(self):
        with patch("argparse.ArgumentParser.parse_args", return_value=Namespace(username="fixture", github_cli=False, render_snapshot=False)), \
             patch.object(activity, "fetch_calendar", side_effect=RuntimeError("Network unavailable")), \
             patch.object(activity, "write_assets") as write:
            with self.assertRaisesRegex(RuntimeError, "Network unavailable"):
                activity.main()
            write.assert_not_called()

    def test_offline_redraw_preserves_saved_dates_and_never_fetches(self):
        data = activity.normalize_calendar(self.calendar, self.today)
        data.update(username="fixture", updated=self.today.isoformat())
        with TemporaryDirectory() as directory:
            snapshot = Path(directory) / "activity-data.json"
            original = json.dumps(data)
            snapshot.write_text(original, encoding="utf-8")
            with patch.object(activity, "ASSETS", Path(directory)), \
                 patch("sys.argv", ["update_activity.py", "--render-snapshot"]), \
                 patch.object(activity, "fetch_calendar") as fetch, \
                 patch.object(activity, "write_assets") as write:
                activity.main()
            fetch.assert_not_called()
            self.assertEqual(snapshot.read_text(encoding="utf-8"), original)
            outputs = write.call_args.args[0]
            self.assertEqual(len(outputs), 2)
            for output in outputs.values():
                self.assertIn("Updated 2025-12-31 UTC", output)

    def test_offline_redraw_rejects_inflated_snapshot_without_writing(self):
        data = activity.normalize_calendar(self.calendar, self.today)
        data.update(username="fixture", updated=self.today.isoformat(), total=999)
        with TemporaryDirectory() as directory:
            (Path(directory) / "activity-data.json").write_text(json.dumps(data), encoding="utf-8")
            with patch.object(activity, "ASSETS", Path(directory)), \
                 patch("sys.argv", ["update_activity.py", "--render-snapshot"]), \
                 patch.object(activity, "write_assets") as write:
                with self.assertRaisesRegex(ValueError, "total"):
                    activity.main()
            write.assert_not_called()

    def test_partial_month_does_not_hide_the_next_month_label(self):
        start = date(2025, 9, 28)
        days = [{"date": (start + timedelta(days=i)).isoformat(), "count": 0, "level": 0} for i in range(21)]
        grid = activity.calendar_grid(activity.weeks_from_days(days), 78, 182, 20)
        self.assertIn(">Oct</text>", grid)
        self.assertNotIn(">Sep</text>", grid)


if __name__ == "__main__":
    unittest.main()
