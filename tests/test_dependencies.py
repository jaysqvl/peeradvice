"""Real database tests, restricted to an explicitly disposable local database."""
import contextlib
import os
from pathlib import Path
import unittest
from urllib.parse import parse_qs, urlsplit

import psycopg2
import psycopg2.extras


TEST_DSN = os.environ.get("TEST_DATABASE_URL", "")
_target = urlsplit(TEST_DSN)
if (_target.scheme not in {"postgres", "postgresql"}
        or _target.hostname not in {"localhost", "127.0.0.1"}
        or _target.path != "/peeradvice_dependency_tests"
        or _target.query or _target.fragment):
    raise RuntimeError("Tests require a loopback TEST_DATABASE_URL for peeradvice_dependency_tests, without query overrides")
os.environ["DATABASE_URL"] = TEST_DSN

# Import only after the connection target has been checked. No live provider calls.
import server


class DependencyContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = Path(__file__).resolve().parents[1].joinpath("setup.sql").read_text()
        with contextlib.closing(psycopg2.connect(TEST_DSN)) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS students, advisors")
                cursor.execute(schema)
            conn.commit()
        server.app.config.update(TESTING=True)

    def setUp(self):
        with contextlib.closing(psycopg2.connect(TEST_DSN)) as conn:
            with conn.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE students, advisors")
            conn.commit()
        self.client = server.app.test_client()

    def row(self, table, uid):
        self.assertIn(table, {"students", "advisors"})
        with contextlib.closing(psycopg2.connect(TEST_DSN)) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM " + table + " WHERE uid = %s", (uid,))
                return cursor.fetchone()

    def create(self, role, uid, name="Fixture Person", email="fixture@example.invalid"):
        return self.client.get("/" + role, query_string={"uid": uid, "name": name, "email": email})

    def test_advisor_creation_existing_profile_and_escaping(self):
        name = '<script>alert("fixture")</script>'
        response = self.create("advisor", "advisor-1", name)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn(name, html)
        self.assertEqual(self.row("advisors", "advisor-1")["name"], name)
        repeated = self.create("advisor", "advisor-1", "Do not overwrite")
        self.assertEqual(repeated.status_code, 200)
        self.assertEqual(self.row("advisors", "advisor-1")["name"], name)

    def test_student_creation_existing_profile_and_parameterized_uid(self):
        uid = "student'; DROP TABLE advisors; --"
        response = self.create("student", uid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.row("students", uid)["name"], "Fixture Person")
        self.assertEqual(self.create("student", uid, "Do not overwrite").status_code, 200)
        self.assertEqual(self.row("students", uid)["name"], "Fixture Person")
        self.assertEqual(self.create("advisor", "still-works").status_code, 200)

    def test_advisor_update_uses_real_driver_and_preserves_redirect(self):
        self.create("advisor", "advisor-1")
        fields = {"uid": "advisor-1", "name": "Updated Advisor", "degree": "BSc",
                  "major": "Computer Science", "minor": "Math", "year_level": "3",
                  "calendly_link": "https://calendly.example.invalid/fixture",
                  "bio": "Synthetic profile", "email": "updated@example.invalid"}
        response = self.client.post("/editadvisor", data=fields)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response.headers["Location"]).path, "/advisor")
        self.assertEqual(parse_qs(urlsplit(response.headers["Location"]).query), {
            "uid": ["advisor-1"], "name": ["Updated Advisor"], "email": ["updated@example.invalid"]})
        row = self.row("advisors", "advisor-1")
        for key, value in fields.items():
            self.assertEqual(row[key], int(value) if key == "year_level" else value)
        self.assertIn("Synthetic profile", self.create("advisor", "advisor-1").get_data(as_text=True))

    def test_student_update_uses_real_driver_and_preserves_redirect(self):
        self.create("student", "student-1")
        fields = {"uid": "student-1", "name": "Updated Student", "degree": "BA",
                  "major": "Economics", "minor": "Math", "year_level": "2",
                  "email": "student@example.invalid"}
        response = self.client.post("/editstudent", data=fields)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response.headers["Location"]).path, "/student")
        self.assertEqual(parse_qs(urlsplit(response.headers["Location"]).query), {
            "uid": ["student-1"], "name": ["Updated Student"], "email": ["student@example.invalid"]})
        row = self.row("students", "student-1")
        for key, value in fields.items():
            self.assertEqual(row[key], int(value) if key == "year_level" else value)
        self.assertIn("Economics", self.create("student", "student-1").get_data(as_text=True))

    def test_advisor_listing_uses_real_dict_cursor(self):
        self.create("advisor", "advisor-1", "First Advisor")
        self.create("advisor", "advisor-2", "Second Advisor")
        self.assertEqual({row["uid"] for row in server.getAllAdvisors()}, {"advisor-1", "advisor-2"})
        response = self.client.get("/connectStudent")
        self.assertEqual(response.status_code, 200)
        self.assertIn("First Advisor", response.get_data(as_text=True))
        self.assertIn("Second Advisor", response.get_data(as_text=True))

    def test_static_routes_and_method_rejection(self):
        for route in ["/", "/connectAdvisor", "/appointmentStudent"]:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertIn("<!DOCTYPE html>", response.get_data(as_text=True))
        self.assertEqual(self.client.get("/editadvisor").status_code, 405)
        self.assertEqual(self.client.get("/editstudent").status_code, 405)

    def test_cors_preflight_keeps_the_existing_no_credentials_policy(self):
        response = self.client.options("/editadvisor", headers={
            "Origin": "https://fixture.example.invalid",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "https://fixture.example.invalid")
        self.assertIn("POST", response.headers["Access-Control-Allow-Methods"])
        self.assertEqual(response.headers["Access-Control-Allow-Headers"].lower(), "content-type")
        self.assertNotIn("Access-Control-Allow-Credentials", response.headers)


if __name__ == "__main__":
    unittest.main()
