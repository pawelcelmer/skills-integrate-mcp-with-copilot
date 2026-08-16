import unittest
from unittest.mock import patch

from fastapi import HTTPException

from src.app import signup_for_activity


class SignupCapacityTests(unittest.TestCase):
    def test_signup_succeeds_below_capacity(self):
        activity = {
            "max_participants": 2,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict("src.app.activities", {"Test Activity": activity}):
            result = signup_for_activity("Test Activity", "new@mergington.edu")

        self.assertEqual(result["message"], "Signed up new@mergington.edu for Test Activity")
        self.assertIn("new@mergington.edu", activity["participants"])

    def test_signup_is_rejected_at_capacity(self):
        activity = {
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict("src.app.activities", {"Test Activity": activity}):
            with self.assertRaises(HTTPException) as context:
                signup_for_activity("Test Activity", "new@mergington.edu")

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Activity is full")
        self.assertNotIn("new@mergington.edu", activity["participants"])


if __name__ == "__main__":
    unittest.main()