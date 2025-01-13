import unittest
import subprocess
import os

class TestLogParsingUtility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary test log file
        cls.test_file = "test.log"
        with open(cls.test_file, "w") as f:
            f.writelines([
                "2025-01-12 08:12:34 Starting application service...\n",
                "2025-01-12 08:12:36 Connection established from 192.168.0.101\n",
                "2025-01-12 08:13:05 User 'admin' logged in from 10.0.0.25\n",
                "2025-01-12 08:14:22 Failed login attempt from 203.0.113.45\n",
                "2025-01-12 08:15:47 Database query executed in 123ms\n",
                "2025-01-12 08:17:59 Warning: Memory usage exceeds 85%\n",
                "2025-01-12 08:18:45 Backup started for volume 'disk1'\n",
                "2025-01-12 08:20:02 Backup completed successfully\n",
            ])
    
    @classmethod
    def tearDownClass(cls):
        # Remove the test file after all tests
        os.remove(cls.test_file)

    def run_command(self, *args):
        # Helper function to run the CLI utility and capture output
        result = subprocess.run(
            ["python", "util.py", *args],
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.returncode

    def test_help(self):
        # Test the help command
        output, code = self.run_command("--help")
        self.assertIn("usage:", output)
        self.assertEqual(code, 0)

    def test_first_lines(self):
        # Test the --first option
        output, code = self.run_command("--first", "3", self.test_file)
        expected = (
            "2025-01-12 08:12:34 Starting application service...\n"
            "2025-01-12 08:12:36 Connection established from 192.168.0.101\n"
            "2025-01-12 08:13:05 User 'admin' logged in from 10.0.0.25"
        )
        self.assertEqual(output, expected)
        self.assertEqual(code, 0)

    def test_last_lines(self):
        # Test the --last option
        output, code = self.run_command("--last", "2", self.test_file)
        expected = (
            "2025-01-12 08:18:45 Backup started for volume 'disk1'\n"
            "2025-01-12 08:20:02 Backup completed successfully"
        )
        self.assertEqual(output, expected)
        self.assertEqual(code, 0)

    def test_timestamps(self):
        # Test the --timestamps option
        output, code = self.run_command("--timestamps", self.test_file)
        self.assertIn("2025-01-12 08:12:34 Starting application service...", output)
        self.assertIn("2025-01-12 08:20:02 Backup completed successfully", output)
        self.assertEqual(code, 0)

    def test_ipv4(self):
        # Test the --ipv4 option
        output, code = self.run_command("--ipv4", self.test_file)
        self.assertIn("192.168.0.101", output)
        self.assertIn("10.0.0.25", output)
        self.assertEqual(code, 0)

    def test_empty_file(self):
        # Test behavior with an empty file
        with open("empty.log", "w") as f:
            pass  # Create an empty file
        output, code = self.run_command("--first", "3", "empty.log")
        self.assertEqual(output, "")
        self.assertEqual(code, 0)
        os.remove("empty.log")

if __name__ == "__main__":
    unittest.main()
