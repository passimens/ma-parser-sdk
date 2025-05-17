import asyncio
import importlib.util
import os
import unittest
from pathlib import Path


class TestAnyParser(unittest.IsolatedAsyncioTestCase):
    """Common behavior for the tests for any specific parser inheriting from BaseParser/XmlBaseParser."""

    # Subclasses should ideally only define the following class variable, e.g.:
    '''
    parser_meta = {
        "parser_class": IntParser,
        "dataset_dir": "data"
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

    @staticmethod
    def _load_metadata(py_path: Path) -> dict:
        """Dynamically loads the `meta` dict from a .py file."""
        spec = importlib.util.spec_from_file_location(py_path.stem, py_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "meta")

    async def test_parse_stream(self):
        """Test parser_class.parse_stream() with all *.txt datasets and per-file metadata."""
        parser_class = self.parser_meta["parser_class"]
        dataset_dir = Path(self.parser_meta["dataset_dir"])

        for txt_file in sorted(dataset_dir.glob("*.txt")):
            meta_file = txt_file.with_suffix(".py")

            with self.subTest(src_file=str(txt_file)):
                if not meta_file.exists():
                    self.fail(f"Metadata file not found for {txt_file.name}: expected {meta_file.name}")

                meta = self._load_metadata(meta_file)

                self.src_file = txt_file
                self.expected_error = meta["exc"]
                self.expected_data = meta["res"]
                self.parsed_items = []
                self.parser = parser_class(self._in_test_callback)

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