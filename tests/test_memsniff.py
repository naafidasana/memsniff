import io
import unittest
from src.tracker import MemSniff
from unittest.mock import patch


class TestMemSniff(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.memsniff = MemSniff()

    def test_tracking_commenced(self):
        self.memsniff.commence()
        self.assertTrue(self.memsniff.tracking)

    def test_tracking_halted(self):
        self.memsniff.commence()
        self.memsniff.halt()
        self.assertFalse(self.memsniff.tracking)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_memsniff(self, mock_stdout):
        @self.memsniff
        def dummy_func():
            dummy_list = [10] * 100000000

        dummy_func()

        res = mock_stdout.getvalue()
        self.assertIn("Detected Memory Leaks", res)
        self.assertIn("File", res)
        self.assertIn("Line", res)
        self.assertIn("Memory Increase", res)
