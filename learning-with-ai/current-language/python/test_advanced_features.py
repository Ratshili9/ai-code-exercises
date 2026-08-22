import unittest
from idiomatic_transformation import process_active_users_procedural, process_active_users_idiomatic
from advanced_decorators import retry, timing_benchmark, fetch_simulated_api_data

class TestDeepeningLanguageFeatures(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {"id": 1, "username": "  Alice  ", "score": 95, "is_active": True},
            {"id": 2, "username": "BOB", "score": 70, "is_active": True},
            {"id": 3, "username": "charlie", "score": 40, "is_active": True},
            {"id": 4, "username": "david", "score": 85, "is_active": False},  # Inactive
            {"id": 5, "username": "eve", "score": None, "is_active": True}     # None score
        ]

    def test_idiomatic_parity(self):
        procedural_res = process_active_users_procedural(self.sample_data)
        idiomatic_res = process_active_users_idiomatic(self.sample_data)
        
        self.assertEqual(len(procedural_res["users"]), len(idiomatic_res["users"]))
        self.assertEqual(round(procedural_res["average_score"], 2), idiomatic_res["average_score"])
        self.assertEqual(idiomatic_res["users"][0]["tier"], "High")
        self.assertEqual(idiomatic_res["users"][1]["tier"], "Medium")
        self.assertEqual(idiomatic_res["users"][2]["tier"], "Low")

    def test_empty_dataset(self):
        res = process_active_users_idiomatic([])
        self.assertEqual(res["users"], [])
        self.assertEqual(res["average_score"], 0.0)

    def test_retry_decorator_recovery(self):
        fetch_simulated_api_data.attempts = 0
        # Fail first 2 attempts, succeed on 3rd
        result = fetch_simulated_api_data(fail_count=2)
        self.assertEqual(result, "SUCCESS: Payload Received")
        self.assertEqual(fetch_simulated_api_data.attempts, 3)

    def test_retry_decorator_exhaustion(self):
        fetch_simulated_api_data.attempts = 0
        # Fail 3 attempts (exceeds max_attempts=3)
        with self.assertRaises(ConnectionError):
            fetch_simulated_api_data(fail_count=4)

    def test_timing_decorator(self):
        fetch_simulated_api_data.attempts = 0
        fetch_simulated_api_data(fail_count=0)
        self.assertGreaterEqual(fetch_simulated_api_data.last_execution_time, 0.0)

if __name__ == "__main__":
    unittest.main()
