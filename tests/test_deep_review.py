import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, call

from scripts import deep_review


DOCUMENT = "documents/d1"
REVIEW = f"{DOCUMENT}/reviews/r1"
OPERATION = f"operations/{REVIEW}"
QUOTA_URL = "/v1/userQuota"
UPLOAD_URL = "/upload/v1/documents?uploadType=media"
REVIEWS_URL = f"/v1/{DOCUMENT}/reviews"
FREE = {"remainingReviewCount": 1}
PDF = b"%PDF-1.4\nmock paper\n%%EOF"
RESULT = {"name": REVIEW, "result": {"reviewMarkdown": "Full report", "anchoredComments": [{}]}}


class DeepReviewTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        original = Path.cwd()
        os.chdir(directory.name)
        self.addCleanup(os.chdir, original)
        deep_review.PDF.parent.mkdir()
        deep_review.PDF.write_bytes(PDF)

    def run_with(self, responses):
        request = Mock(side_effect=responses)
        deep_review.run(lambda: request, polls=1)
        return request

    def test_zero_quota_only_reads_and_records_next_time(self):
        next_time = "2026-11-29T14:30:00Z"
        request = self.run_with([{"remainingReviewCount": 0, "nextAvailableTime": next_time}])
        request.assert_called_once_with("GET", QUOTA_URL)
        self.assertIn(next_time, deep_review.LOG.read_text(encoding="utf-8"))
        self.assertFalse((deep_review.LOCAL / "deep-review-state.json").exists())

    def test_complete_review_and_rebuild(self):
        request = self.run_with([
            FREE, {"name": DOCUMENT}, FREE, {"name": OPERATION},
            {"done": True, "response": {"name": REVIEW}}, RESULT,
        ])
        self.assertEqual(request.call_args_list, [
            call("GET", QUOTA_URL),
            call("POST", UPLOAD_URL, PDF, "application/pdf"),
            call("GET", QUOTA_URL),
            call("POST", REVIEWS_URL, b'{"runConfig":{"topology":"MID"}}', "application/json"),
            call("GET", f"/v1/{OPERATION}"),
            call("GET", f"/v1/{REVIEW}"),
        ])
        digest = hashlib.sha256(PDF).hexdigest()
        self.assertEqual((deep_review.LOCAL / f"reviewed-{digest}.pdf").read_bytes(), PDF)
        result_path = deep_review.LOCAL / "deep-review.json"
        self.assertEqual(json.loads(result_path.read_text(encoding="utf-8")), RESULT)
        self.assertIn(digest, deep_review.LOG.read_text(encoding="utf-8"))
        deep_review.PDF.write_bytes(PDF + b"rebuilt")
        factory = Mock()
        deep_review.run(factory)
        factory.assert_not_called()

    def test_resume_saved_operation(self):
        self.run_with([FREE, {"name": DOCUMENT}, FREE, {"name": OPERATION}, {"done": False}])
        request = self.run_with([{"done": True, "response": {"name": REVIEW}}, RESULT])
        self.assertEqual(request.call_args_list, [call("GET", f"/v1/{OPERATION}"), call("GET", f"/v1/{REVIEW}")])

    def test_ambiguous_submission_checks_existing_reviews(self):
        with self.assertRaises(TimeoutError):
            self.run_with([FREE, {"name": DOCUMENT}, FREE, TimeoutError()])
        request = self.run_with([{}])
        request.assert_called_once_with("GET", REVIEWS_URL)
        request = self.run_with([
            {"reviews": [{"name": REVIEW}]}, {"done": True, "response": {"name": REVIEW}}, RESULT,
        ])
        self.assertEqual(request.call_args_list, [
            call("GET", REVIEWS_URL), call("GET", f"/v1/{OPERATION}"), call("GET", f"/v1/{REVIEW}"),
        ])


if __name__ == "__main__":
    unittest.main()
