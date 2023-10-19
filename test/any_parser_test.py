import asyncio
import unittest
from parser_api.example.copy_parser import CopyParser
import os


class TestAnyParser(unittest.IsolatedAsyncioTestCase):
    """Common behavior for the tests for any specific parser inheriting from BaseParser/XmlBaseParser."""

    # Subclasses should ideally override only the following class variable:
    parser_meta = {
        "parser_class": CopyParser,
        "dataset": {
            # <src_file>: [<expected_items>]
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            "data/test_data_1.txt": ["1", "1", "2", "3", "5", "8", "13", "21", "34"],
            "data/test_data_2.txt": ["abc", "cde", "efg", "ghi", "ijk", "klm", "mno", "opq", "qrs"],
            },
        }

    async def _in_test_callback(self, items):
        """Callback function for use in tests."""
        self.parsed_items.extend(items)

    async def asyncSetUp(self) -> None:
        self.parsed_items = []
        self.parser = self.parser_meta["parser_class"](self._in_test_callback)
        self.fifo_path = "test_fifo"
        os.mkfifo(self.fifo_path)
        self.src_file = os.getenv("PARSER_SRC_FILE", self.parser_meta["dataset"].keys().__iter__().__next__())

    async def asyncTearDown(self) -> None:
        os.remove(self.fifo_path)

    async def test_parse_stdin(self):
        """Tests <SomeParser>.parse_stdin()."""
        print(f"Parsing data from stdin, expecting contents of {self.src_file}...")
        waited = 0
        task = asyncio.create_task(self.parser.parse_stdin())
        while waited < 10:
            await asyncio.sleep(0.1)
            if len(self.parsed_items) >= len(self.parser_meta["dataset"][self.src_file]):
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, self.parser_meta["dataset"][self.src_file])

    async def test_parse_fifo(self):
        """Tests <SomeParser>.parse_fifo()."""
        print("Running a command which would return text to parse via a named pipe...")
        proc = await asyncio.create_subprocess_shell(
            f"cat {self.src_file} > {self.fifo_path}",
            )
        print(f"Parsing data from named pipe {self.fifo_path}... ")
        waited = 0
        task = asyncio.create_task(self.parser.parse_fifo(self.fifo_path))
        while waited < 10:
            await asyncio.sleep(0.1)
            if len(self.parsed_items) >= len(self.parser_meta["dataset"][self.src_file]):
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, self.parser_meta["dataset"][self.src_file])

    async def test_parse_stream(self):
        """Tests <SomeParser>.parse_stream()."""
        print("Running a command which would return text to parse via subprocess.PIPE...")
        proc = await asyncio.create_subprocess_shell(
            f"cat {self.src_file}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
        waited = 0
        task = asyncio.create_task(self.parser.parse_stream(proc.stdout))
        while waited < 10:
            await asyncio.sleep(0.1)
            if len(self.parsed_items) >= len(self.parser_meta["dataset"][self.src_file]):
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, self.parser_meta["dataset"][self.src_file])


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
