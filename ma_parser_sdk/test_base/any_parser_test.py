import asyncio
import unittest
import os
import stat


class TestAnyParser(unittest.IsolatedAsyncioTestCase):
    """Common behavior for the tests for any specific parser inheriting from BaseParser/XmlBaseParser."""

    # Subclasses should ideally only define the following class variable, e.g.:
    '''
    parser_meta = {
        "parser_class": IntParser,
        "dataset": {
            # <src_file>: { 'exc': <expected_exception>, 'res': [<expected_items>] }
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            # for invalid <src_file> expected error should be specified in 'exc' field
            "data/int_data_1.txt": {
                "exc": None,
                # "res": ["1", "1", "2", "3", "5", "8", "13", "21", "34"],
                "res": [1, 1, 2, 3, 5, 8, 13, 21, 34],
                },
            "data/str_data_1.txt": {
                "exc": ValueError,
                "res": ["abc", "cde", "efg", "ghi", "ijk", "klm", "mno", "opq", "qrs"],
                },
            },
        }
    '''
    # In some cases it may be necessary to override _verify_parsed_items method

    def _verify_parsed_items(self) -> None:
        """Validates the parsed items against the expected items."""
        self.assertEqual(self.parsed_items, self.expected_data)

    async def _wait_for_parsing_task(self, task):
        """Waits for the parsing task to complete."""
        waited = 0
        while waited < 10:
            await asyncio.sleep(0.1)
            if task.done():
                break
            if len(self.parsed_items) >= len(self.expected_data):
                break
            waited += 1
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    async def _in_test_callback(self, items):
        """Callback function for use in tests."""
        self.parsed_items.extend(items)

    async def asyncSetUp(self) -> None:
        self.parsed_items = []
        self.parser = self.parser_meta["parser_class"](self._in_test_callback)
        self.src_file = os.getenv("PARSER_SRC_FILE", self.parser_meta["dataset"].keys().__iter__().__next__())
        self.expected_error = self.parser_meta["dataset"][self.src_file]["exc"]
        self.expected_data = self.parser_meta["dataset"][self.src_file]["res"]

    async def asyncTearDown(self) -> None:
        pass

    async def test_parse_stream(self):
        """Tests <SomeParser>.parse_stream()."""
        print(f"Sending contents of {self.src_file} to subprocess.PIPE...")
        proc = await asyncio.create_subprocess_shell(
            f"cat {self.src_file}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
        task = asyncio.create_task(self.parser.parse_stream(proc.stdout))
        if self.expected_error is not None:
            with self.assertRaises(self.expected_error):
                await self._wait_for_parsing_task(task)
        else:
            await self._wait_for_parsing_task(task)
            self._verify_parsed_items()
