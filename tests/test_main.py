import contextlib
import io
import os
import unittest
from unittest.mock import patch

import main


class MainTests(unittest.TestCase):
    def test_health_check_reports_local_helpers(self):
        report = main.health_check()
        self.assertEqual(report["status"], "ok")
        self.assertTrue(all(report["helpers_present"].values()))

    def test_check_mode_is_runnable_without_secret(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main.main(["--check"])
        self.assertEqual(result, 0)
        self.assertIn('"status": "ok"', output.getvalue())

    def test_normal_mode_explains_missing_secret(self):
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(output):
            result = main.main([])
        self.assertEqual(result, 2)
        self.assertIn("EPSILON_GROQ", output.getvalue())


if __name__ == "__main__":
    unittest.main()
