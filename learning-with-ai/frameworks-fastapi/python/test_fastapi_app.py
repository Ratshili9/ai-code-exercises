import unittest
from fastapi.testclient import TestClient
import sys, os

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))
from app.main import app, todos_db

class TestFastAPITodoAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        todos_db.clear()

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_create_and_get_todo(self):
        payload = {"title": "Learn FastAPI with AI", "description": "Complete curriculum exercises"}
        response = self.client.post("/todos/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Learn FastAPI with AI")
        self.assertFalse(data["completed"])
        todo_id = data["id"]

        get_res = self.client.get(f"/todos/{todo_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["id"], todo_id)

    def test_update_todo_status(self):
        # Create
        create_res = self.client.post("/todos/", json={"title": "Test Task"})
        todo_id = create_res.json()["id"]

        # Patch completed = True
        patch_res = self.client.patch(f"/todos/{todo_id}", json={"completed": True})
        self.assertEqual(patch_res.status_code, 200)
        self.assertTrue(patch_res.json()["completed"])

    def test_list_and_filter_todos(self):
        self.client.post("/todos/", json={"title": "Pending 1", "completed": False})
        self.client.post("/todos/", json={"title": "Done 1", "completed": True})

        # List all
        all_res = self.client.get("/todos/")
        self.assertEqual(len(all_res.json()), 2)

        # Filter completed
        done_res = self.client.get("/todos/?completed=true")
        self.assertEqual(len(done_res.json()), 1)
        self.assertEqual(done_res.json()[0]["title"], "Done 1")

    def test_delete_todo(self):
        create_res = self.client.post("/todos/", json={"title": "Delete me"})
        todo_id = create_res.json()["id"]

        del_res = self.client.delete(f"/todos/{todo_id}")
        self.assertEqual(del_res.status_code, 204)

        get_res = self.client.get(f"/todos/{todo_id}")
        self.assertEqual(get_res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
