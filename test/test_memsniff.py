import unittest
from src.tracker import MemSniff


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
        self.assertTrue(self.memsniff.tracking)

    def test_memsniff(self, capsys):
        @self.memsniff
        def dummy_func():
            dummy_list = [10] * 100000000

        dummy_func()

        res = capsys.readouterr()
        self.assertIn("Detected Memory Leaks:", res.out)
        self.assertIn("File:", res.out)
        self.assertIn("Line:", res.out)
        self.assertIn("Memory Increase:", res.out)


if __name__ == "__main__":
    unittest.main()
